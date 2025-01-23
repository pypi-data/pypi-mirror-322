import hashlib
from typing import List


def file_md5(file_path: str) -> str:
    """
    Compute the MD5 hash of the file content.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()