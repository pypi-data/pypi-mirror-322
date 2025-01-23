"""Context management module for handling file operations and tracking changes."""

import hashlib
import logging
import os
import shutil

from herotools.pathtools import remove_file_if_exists
from herotools.texttools import name_fix


class MyFile:
    """A class representing a file in the context system with tracking capabilities."""

    def __init__(self, path: str):
        """Initialize a MyFile instance.

        Args:
            path: The path to the file

        """
        self.path = path
        self.exists = os.path.exists(self.path)
        self.changed_in_context = False  # Indicates if the file is new or was changed
        self._md5 = ""

    def md5(self) -> str:
        """Calculate and return MD5 hash of the file.

        Returns:
            str: The MD5 hash of the file's contents

        Raises:
            FileNotFoundError: If the file does not exist

        """
        if not self.exists:
            raise FileNotFoundError(f"File does not exist: {self.path}")
        if not self._md5:
            with open(self.path, "rb") as file:
                self._md5 = hashlib.md5(file.read()).hexdigest()
        return self._md5

    def name(self) -> str:
        """Return the base name of the file.

        Returns:
            str: The file's base name

        """
        return os.path.basename(self.path)

    def ext(self) -> str:
        """Return the file extension in lower case.

        Returns:
            str: The file's extension in lowercase

        """
        return os.path.splitext(self.path)[1].lower()


class Context:
    """A class for managing file contexts and tracking file changes."""

    def __init__(self, name: str = "default", reset: bool = False):
        """Initialize a Context instance.

        Args:
            name: The name of the context
            reset: Whether to reset (remove) the existing context

        """
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        self.logger = logging.getLogger(__name__)
        contextroot = os.getenv("CONTEXTROOT", "~/context")
        self.name = name_fix(name)
        self.path = os.path.join(os.path.expanduser(contextroot), self.name)
        if reset:
            self._remove_context()

    def _remove_context(self):
        """Remove the context directory if it exists."""
        if os.path.exists(self.path):
            try:
                shutil.rmtree(self.path)
                self.logger.info(f"Context directory removed: {self.path}")
            except Exception as e:
                self.logger.error(f"Error removing context directory: {e!s}")

    def file_set(self, path: str, cat: str, name: str = "", content: str = "") -> MyFile:
        """Set a file in the context with the given category.

        Args:
            path: Source file path
            cat: Category for organizing files
            name: Optional custom name for the file
            content: Optional content to write to file

        Returns:
            MyFile: A MyFile instance representing the file in context

        Raises:
            ValueError: If both path and content are provided
            FileNotFoundError: If the source file does not exist

        """
        cat = name_fix(cat)
        name = name_fix(name)

        if content:
            if path:
                raise ValueError("path and content cannot be both set")
            path = os.path.join(self.path, "files", cat, name)
            with open(path, "w") as file:
                file.write(content)

        mf = MyFile(path=path)
        if not mf.exists:
            raise FileNotFoundError(f"Source file does not exist: {path}")

        if not content:
            if not name:
                name = name_fix(mf.name())
            else:
                if os.path.splitext(name)[1].lower() != mf.ext():
                    name_ext = os.path.splitext(name)[1]
                    raise ValueError(f"Extension {name_ext} must match file extension {mf.ext()}")

        file_path = os.path.join(self.path, "files", cat, name)
        file_path_md5 = os.path.join(self.path, "files", cat, name + ".md5")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Check if the MD5 hash of the file on disk
        md5_on_disk = ""
        if os.path.exists(file_path_md5):
            with open(file_path_md5) as file:
                md5_on_disk = file.read().strip()
            # Validate that it's a valid MD5 hash
            if len(md5_on_disk) != 32 or not all(c in "0123456789abcdef" for c in md5_on_disk.lower()):
                raise RuntimeError("Bug: hash is not in the right format")

        new_md5 = mf.md5()

        changed_in_context = False
        if not md5_on_disk or new_md5 != md5_on_disk:
            changed_in_context = True

        md5_dir = os.path.join(self.path, "files", "md5")

        if changed_in_context:
            # File did change
            old_name = os.path.basename(path)
            new_name = os.path.basename(file_path)
            self.logger.debug(f"File changed in context {self.name}: {old_name} -> {new_name}")
            if mf.path != file_path:
                shutil.copy2(mf.path, file_path)
            with open(file_path_md5, "w") as file:
                file.write(new_md5)
            # Remove the old MD5 link if it exists
            if md5_on_disk:
                old_md5_link = os.path.join(md5_dir, md5_on_disk)
                remove_file_if_exists(old_md5_link)

        mf.path = file_path

        os.makedirs(md5_dir, exist_ok=True)
        md5_link = os.path.join(md5_dir, mf.md5())
        if not os.path.exists(md5_link):
            os.symlink(os.path.relpath(file_path, md5_dir), md5_link)

        return mf

    def file_get(self, name: str, cat: str, needtoexist: bool = True) -> MyFile:
        """Get a file from the context with the given category.

        Args:
            name: Name of the file to retrieve
            cat: Category the file is stored under
            needtoexist: Whether to raise an error if file doesn't exist

        Returns:
            MyFile: A MyFile instance representing the requested file

        Raises:
            FileNotFoundError: If needtoexist is True and file doesn't exist

        """
        name = name_fix(name)
        cat = name_fix(cat)
        file_path = os.path.join(self.path, "files", cat, name)
        if needtoexist:
            if os.path.exists(file_path):
                return MyFile(file_path)
            else:
                self.logger.warning(f"File not found: {file_path}")
                raise FileNotFoundError(f"Context file does not exist: {file_path}")
        else:
            return MyFile(file_path)
