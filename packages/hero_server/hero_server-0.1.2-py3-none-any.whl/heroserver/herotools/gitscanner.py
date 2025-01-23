import sys
import os

# Add the parent directory of herotools to the Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import json
import subprocess
from typing import Optional,List
import redis
from herotools.logger import logger
from herotools.texttools import name_fix
from enum import Enum, auto
from dataclasses import dataclass
import git


# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Define the ChangeType Enum
class ChangeType(Enum):
    DEL = 'del'
    MOD = 'mod'
    NEW = 'new'

@dataclass
class FileChange:
    commit_hash: str
    commit_time: str
    path: str #relative path in the repo
    change_type: ChangeType


class Repo:
    def __init__(self, cat: str, account: str, name: str, path: str):
        self.cat = cat
        self.account = account
        self.name = name
        self.path = path
        self.hash_last_found: Optional[float] = None
        self.hash_last_processed: Optional[str] = None
        self.lastcheck: Optional[float] = None

    def __str__(self):
        return json.dumps({
            "cat": self.cat,
            "account": self.account,
            "name": self.name,
            "path": self.path,
            "hash_last_found": self.hash_last_found,
            "hash_last_processed": self.hash_last_processed,
            "lastcheck": self.lastcheck
        }, indent=2)

    def _redis_key(self) -> str:
        return f"gitcheck:{self.cat}:{self.account}:{self.name}"

    def save_to_redis(self):
        redis_client.set(self._redis_key(), json.dumps(self.__dict__))

    @staticmethod
    def load_from_redis(cat: str, account: str, name: str) -> Optional['Repo']:
        redis_key = f"gitcheck:{cat}:{account}:{name}"
        data = redis_client.get(redis_key)
        if data:
            data = json.loads(data)
            repo = Repo(data["cat"], data["account"], data["name"], data["path"])
            repo.hash_last_found = data.get("hash_last_found")
            repo.hash_last_processed = data.get("hash_last_processed")
            repo.lastcheck = data.get("lastcheck")
            return repo
        return None

    def get_remote_commit_hash(self, branch: str) -> str:
        """Get the latest commit hash from the remote repository."""
        result = subprocess.run(
            ['git', 'ls-remote', 'origin', f'refs/heads/{branch}'],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error fetching remote commit hash: {result.stderr}")
        
        return result.stdout.split()[0]

    def get_local_commit_hash(self) -> str:
        """Get the latest commit hash from the local repository."""
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error fetching local commit hash: {result.stderr}")
        
        return result.stdout.strip()

    def get_current_branch(self) -> str:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error fetching local branch name: {result.stderr}")

        return result.stdout.split()[0]

    def get_remote_default_branch(self) -> str:
        result = subprocess.run(
            ['git', 'ls-remote', '--symref', 'origin', 'HEAD'],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error fetching local branch name: {result.stderr}")

        return result.stdout.split()[1].split('/')[-1]

    def should_check_again(self) -> bool:
        """Determine if we should check the repository again based on the last check time."""
        if self.lastcheck is None:
            return True
        return (time.time() - self.lastcheck) > 60

    def update_last_check_time(self) -> None:
        """Update the last check time."""
        self.lastcheck = time.time()
        self.save_to_redis()

    def log_change(self, epoch_time: float) -> None:
        """Log a detected change in Redis."""
        self.hash_last_found = epoch_time
        self.save_to_redis()

    def check_for_changes(self, branch: str = 'main') -> None:
        """Check the repository for updates and log changes if found."""
        if not self.should_check_again():
            print("WAIT TO CHECK FOR CHANGES")
            return

        try:
            diff_commits = self.get_local_remote_diff_commits(branch)

            if diff_commits != []:
                print("FOUND SOME CHANGES")
                self.log_change(time.time())
                file_changes = self.get_file_changes_from_commits(diff_commits)
                self.print_file_changes(file_changes)
            else:
                print("NO CHANGED FOUND")

            self.update_last_check_time()
        except Exception as e:
            print(f"An error occurred while checking repo {self.path}: {e}")
            
    def get_local_remote_diff_commits(self, branch: str) -> List[git.Commit]:
        # Open the repository
        repo = git.Repo(self.path)

        # Get the local branch
        local_branch = repo.heads[branch]
        # Get the remote reference for the branch
        remote_ref = repo.remotes.origin.refs[branch]

        # Fetch the latest changes from the remote
        repo.remotes.origin.fetch()

        # Get the commit hashes of the local and remote branches
        local_commit = local_branch.commit
        remote_commit = remote_ref.commit

        if local_commit == remote_commit:
            return []

        # Get the common ancestor commit
        base_commit = repo.merge_base(local_commit, remote_commit)[0]

        # Get the ahead and behind commits
        ahead_commits = list(repo.iter_commits(f"{base_commit}..{local_commit}"))
        behind_commits = list(repo.iter_commits(f"{base_commit}..{remote_commit}"))

        # Combine the ahead and behind commits
        diff_commits = ahead_commits + behind_commits
        return diff_commits

    def get_file_changes_from_commits(self, commit_list: List[git.Commit]) -> List[FileChange]:
        file_changes = []
        for commit in commit_list:
            # print(commit)
            diffs = commit.diff(self.hash_last_processed, create_patch=True)
            # print(diffs)
            for diff in diffs:
                if diff.deleted_file:
                    change_type = ChangeType.DEL
                elif diff.new_file:
                    change_type = ChangeType.NEW
                else:
                    change_type = ChangeType.MOD

                file_change = FileChange(
                    commit_hash=commit.hexsha,
                    commit_time=str(commit.committed_datetime),
                    path=diff.b_path if diff.new_file else diff.a_path,
                    change_type=change_type
                )
                file_changes.append(file_change)
        return file_changes
    
    def print_file_changes(self, file_changes: List[FileChange]):
        for file_change in file_changes:
            print("------------------------------------")
            print(f"Commit Hash: {file_change.commit_hash}")
            print(f"Commit Time: {file_change.commit_time}")
            print(f"File Path: {file_change.path}")
            print(f"Change Type: {file_change.change_type.value}")
            print("------------------------------------")

def gitscan(path: str, cat: str) -> None:
    """Walk over directories to find Git repositories and check them."""
    path = os.path.abspath(os.path.expanduser(path))
    for root, dirs, files in os.walk(path):
        if '.git' in dirs:
            accountname = os.path.basename(os.path.dirname(root))
            reponame = os.path.basename(root)
            repo = Repo.load_from_redis(cat, accountname, reponame)
            if repo is None:
                repo = Repo(cat, accountname, reponame, root)
            branch = repo.get_current_branch()

            logger.debug(f"root: {root}")
            logger.debug(f"accountname: {accountname}")
            logger.debug(f"reponame: {reponame}")
            logger.debug(f"branch: {branch}")
            logger.debug(f"repo: {repo}")
            
            repo.check_for_changes(branch)
            dirs[:] = []  # Don't go deeper into subdirectories
        else:
            # Filter out any .git directories from further traversal
            dirs[:] = [d for d in dirs if d != '.git']

def print_redis_client():
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor)
        for key in keys:
            value = redis_client.get(key)
            print(key)
            print(value)
            print()
        if cursor == 0:
            break

if __name__ == "__main__":
    # print_redis_client()
    mypath = "~/code/git.ourworld.tf/projectmycelium"
    category = 'mycat'
    gitscan(path=mypath, cat=category)
    # print_redis_client()