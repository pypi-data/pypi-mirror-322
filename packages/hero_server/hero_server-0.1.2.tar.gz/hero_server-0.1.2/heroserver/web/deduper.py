import hashlib
from typing import Dict
import os
from pathlib import Path
import json
import shutil

class Deduper:
    """
    Tools to start from an existing directory to make sure we don't have duplicates in template
    """
    def __init__(self, path: str):
        self.path = Path(path).expanduser().resolve()
        self.path.mkdir(parents=True, exist_ok=True)
        self.hash_dict: Dict[str, str] = {} #key is the hash, #value is the relative path of the object in relation to the deduper
        self.meta_file = self.path / ".meta.json"
        
        #from IPython import embed;embed()
        
        if self.meta_file.exists():
            self.import_dict()
        else:
            self.load_assets()

    def load_assets(self):
        """Load all the existing files and calculate their hashes"""
        self.hash_dict = {}
        for root, _, files in os.walk(self.path):            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.path)                
                print(f" - load deduped file {file_path}")
                if not file.startswith('.'):
                    file_hash = self._calculate_md5(file_path)
                    if file_hash in self.hash_dict:
                        raise Exception(f"duplicate in dedupe pool: {file_path}")
                    self.hash_dict[file_hash] = relative_path
        self.export_dict()

    def _calculate_md5(self, file_path: str) -> str:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def export_dict(self):
        """Export the hash dictionary to a JSON file"""
        with open(self.meta_file, 'w') as f:
            json.dump(self.hash_dict, f, indent=2)

    def import_dict(self):
        """Import the hash dictionary from a JSON file"""
        with open(self.meta_file, 'r') as f:
            self.hash_dict = json.load(f)
            
            
    def path_check(self, path: str = "") -> str:
        """
        Calculate MD5 from the path to look up the file in the deduper.
        Will return empty string if not found
        """
        file_path = Path(path)
        if not file_path.exists():
            print(f" **ERROR: File '{path}' does not exist.")
            return ""
            # raise FileNotFoundError(f"File '{path}' does not exist.")
        file_hash = self._calculate_md5(str(file_path))        
        return  self.path_find(file_hash=file_hash)

    def path_find(self, path: str = "",file_hash: str = "") -> str:
        """
        return the relative path of the found object in relation to the dedupe stor
        will return empty string if not found
        """
        res = []
        if path!="":
            input_path = Path(path)
            input_filename = input_path.name
            for _, stored_path in self.hash_dict.items():
                stored_path_path = Path(stored_path)
                if stored_path_path.name.lower() == input_filename.lower():
                    if len(input_path.parts) == 1:
                        res.append(stored_path)
                    elif input_path.as_posix().lower() == stored_path_path.as_posix().lower():
                        res.append(stored_path)
            if len(res)==1:
                return res[0]
            elif len(res)==0:
                return ""
            else:
                raise Exception(f"found more than 1: {path}")
        elif file_hash!="":
            if file_hash in self.hash_dict:
                return self.hash_dict[file_hash]
            return ""                
        else:
            raise Exception("need to input path or file_hash")
    
    def add(self, source_path: str, dest_path_rel: str = "",dest_dir_rel = "") -> str:
        """
        Add a file to the specified path in the dedupe pool if it doesn't exist.
        
        Args:
            source_path (str): Path to the source file to be copied.
            dest_path_rel (str): Path where the file should be copied to, relative to the dedupe pool.
        
        Returns:
            str: The path of the file in the dedupe pool if successful, empty string if failed.
        """
        source_path0 = Path(source_path)
        if not dest_path_rel:
            if dest_dir_rel:
                dest_dir_rel=dest_dir_rel.strip("/")
                dest_path_rel = f"{dest_dir_rel}/{source_path0.name}"
            else:
                dest_path_rel = source_path0.name                 
        # dest_path is the relative path

        # Check if the file already exists in the dedupe pool
        existing_path = self.path_check(source_path)
        if existing_path:
            print(f"File already exists in dedupe pool: {existing_path}")
            return existing_path
        dest_path_rel = self._relpath_find_new(dest_path_rel)
        dest_path = self.path / dest_path_rel
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(source_path, dest_path)
            print(f"File copied successfully to: {dest_path}")
        except IOError as e:
            raise Exception(f"Unable to add file {source_path} to {dest_path}.\n{e}")

        # Add the new file to the hash dictionary
        relative_path = dest_path.relative_to(self.path).as_posix()
        file_hash = self._calculate_md5(dest_path.as_posix())
        self.hash_dict[file_hash] = relative_path
        self.export_dict()
        return relative_path

    def path_find_full(self, path: str = "",file_hash: str = "" ) -> str:
        mypath = self.path_find(path=path,file_hash=file_hash)
        return str(self.path / mypath)
    
    
    def _relpath_find_new(self, rel_path: str) -> str:
        """
        find full path which doesn't exist yet
        """
        if not rel_path:
            raise ValueError("rel_path cannot be empty")

        # Construct the full path
        full_path = self.path / rel_path

        # Check if the file exists
        if not full_path.exists():
            return rel_path

        rel_path_obj = Path(rel_path)
        rel_path_no_extension = str(rel_path_obj.with_suffix(''))
        rel_path_extension = rel_path_obj.suffix

        new_rel_path = f"{rel_path_no_extension}{rel_path_extension}"

        # Check if filename exists in the dedupe pool
        counter = 2
        new_full_path = self.path / new_rel_path
        while new_full_path.exists():
            # Update path for the next iteration
            new_rel_path = f"{rel_path_no_extension}_{counter}{rel_path_extension}"
            new_full_path = self.path / new_rel_path
            counter += 1

        return new_rel_path


    def svg_get(self, name: str) -> str:
        """
        Get the SVG content based on the name (in lowercase) and match on the SVG name only.
        
        Args:
            name (str): The name of the SVG file to retrieve.
        
        Returns:
            str: The content of the SVG file if found, empty string otherwise.
        """
        name = Path(name).name.lower()
        name = name.lower()
        if not name.endswith('.svg'):
            name += '.svg'

        for _, stored_path in self.hash_dict.items():
            stored_path_obj = Path(stored_path)
            if stored_path_obj.name.lower() == name:
                full_path = self.path / stored_path
                try:
                    with open(full_path, 'r') as svg_file:
                        return svg_file.read()
                except IOError as e:
                    raise Exception(f"Error reading SVG file {full_path}: {e}")

        raise Exception(f"SVG file '{name}' not found in the dedupe pool.")
