

import os

def expand_path(path: str) -> str:
    """
    Expand ~ to the user's home directory and return the absolute path.
    """
    return os.path.abspath(os.path.expanduser(path))


def remove_file_if_exists(file_path):
    try:
        # This will remove the file or symlink, regardless of whether
        # it's a regular file, a directory, or a broken symlink
        os.remove(file_path)
    except FileNotFoundError:
        # File doesn't exist, so we don't need to do anything
        pass
    except IsADirectoryError:
        # It's a directory, so we use rmdir instead
        os.rmdir(file_path)
    except PermissionError:
        print(f"Permission denied: Unable to remove {file_path}")
    except Exception as e:
        print(f"An error occurred while trying to remove {file_path}: {str(e)}")