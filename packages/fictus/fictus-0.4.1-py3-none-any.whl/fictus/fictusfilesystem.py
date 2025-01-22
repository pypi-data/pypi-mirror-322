"""Contains the class and its methods directly related to the FictusFileSystem."""

import os.path
from pathlib import Path
from typing import Set, Optional

from .fictusexception import FictusException
from .fictusnode import File, Folder, Node

DEFAULT_ROOT_NAME = os.sep


class FictusFileSystem:
    """
    A FictusFileSystem (FFS) simulates the creation and traversal of a file system.
    The FFS allows for the creation and removal of files and folders,
    """

    def __init__(self, name=DEFAULT_ROOT_NAME) -> None:
        self._validate_root(name)
        self._root: Folder = Folder(name, None)
        self._current: Folder = self._root

    @staticmethod
    def _validate_root(name) -> None:
        if name == os.sep or name.endswith(":"):
            return

        raise FictusException(
            f"A root folder must be \"{os.sep}\" or end with a colon, like \"d:\""
        )

    @classmethod
    def init_from_path(cls, path: Path) -> "FictusFileSystem":
        """
        From a given path search for and create a mirrored FFS based on file(s) found on disk.

        @param path: A valid Path.  If a file only adds the file.  If a directory will iterate
                     over all files to build out the FFS.

        @return FictusFileSystem
        """
        ffs = FictusFileSystem(path.drive)

        if path.is_file():
            ffs.add_directory_and_file(path.as_posix())
        else:
            for root, _dirs, files in os.walk(path):

                # Create directories, even if empty
                parts = root.split(os.sep)
                new_root = os.sep.join(parts[1:])
                for d in _dirs:
                    ffs.cd(os.sep)
                    ffs.mkdir(new_root + os.sep + d)

                for file in files:
                    ffs.add_directory_and_file(os.path.join(root, file))

        ffs.cd(path.root)

        return ffs

    def root(self) -> Folder:
        """Return the root of the FFS."""
        return self._root

    def current(self) -> Folder:
        """Return the FFS's current Folder being traversed."""
        return self._current

    @staticmethod
    def _normalize(path: str) -> str:
        return os.path.normpath(path.replace('\\', os.sep))

    @staticmethod
    def _validate(path: str) -> None:
        # will raise if path is empty
        if not path:
            raise FictusException("A path must contain a non-empty string.")

    def mkdir(self, path: str) -> None:
        """Takes a string of a normalized relative to cwd and adds the directories
        one at a time."""

        self._validate(path)

        # hold onto the current directory
        current = self._current

        normalized_path = self._normalize(path)
        if normalized_path.startswith(os.sep):
            self._to_root()
            normalized_path = self._normalize(self._root.value + normalized_path)

        folders = {d.value: d for d in self._current.children}

        for idx, part in enumerate(normalized_path.split(os.sep)):
            if not part:
                continue

            if idx == 0 and part.lower() == self._root.value.lower():
                self._to_root()
                continue

            if part not in folders:
                folders[part] = Folder(part, self._current)
                self._current.children.append(folders[part])

            self.cd(folders[part].value)
            folders = {d.value: d for d in self._current.children}

        # return to starting directory
        self._current = current

    def mkfile(self, *files: str) -> None:
        """Takes one or more filenames and adds them to the cwd."""
        visited: Set[str] = {
            f.value for f in self._current.children if isinstance(f, File)
        }
        for file in files:
            self._validate(file)

            if file not in visited:
                visited.add(file)
                self._current.children.append(File(file, self._current))

    def add_directory_and_file(self, path: str) -> None:
        self._validate(path)

        parts = self._normalize(path).split(os.sep)
        folder = os.sep.join(parts[:-1])
        file = parts[-1]

        self._to_root()  # jump to root
        self.mkdir(folder)  # create dir
        self.cd(folder)  # jump to the directory
        self.mkfile(file)  # create file

    def rename(self, old: str, new: str) -> None:
        """Renames a File or Folder based on its name."""
        for content in self._current.children:
            if content.value == old:
                content.value = new
                break

    def cwd(self) -> str:
        """Prints the current working directory."""
        r = []

        node: Optional[Node] = self._current
        while node is not None:
            r.append(node.value)
            node = node.parent

        return f"{os.sep}".join(reversed(r))

    def _to_root(self) -> None:
        self._current = self._root

    def cd(self, path: str) -> None:
        """Takes a string of a normalized relative to cwd and changes the current"""
        # Return to the current dir if something goes wrong
        current = self._current

        normalized_path = self._normalize(path)
        if normalized_path.startswith(os.sep):
            self._to_root()
            normalized_path = self._normalize(self._root.value + normalized_path)

        for idx, part in enumerate(normalized_path.split(os.sep)):
            if not part:
                continue

            if idx == 0 and part.lower() == self._root.value.lower():
                self._to_root()
                continue

            if part == "..":
                # looking at the parent here, so ensure its valid.
                if isinstance(self._current.parent, Folder):
                    assert isinstance(self._current.parent, Folder) is True  # for typing
                    self._current = self._current.parent
            else:
                hm = {
                    f.value: f for f in self._current.children if isinstance(f, Folder)
                }
                if part not in hm:
                    self._current = current
                    raise FictusException(
                        f"Could not path to {normalized_path} from {self.cwd()}, {part} not a child of {self._current.value}."
                    )

                self._current = hm[part]
