from pathlib import Path
from typing import List
import glob
import os

from pydantic import BaseModel
from typeguard import typechecked

from .base import Storage


class LocalStorageConfig(BaseModel):
    root_directory: Path


class LocalStorage(Storage):
    @typechecked
    def __init__(self, config: LocalStorageConfig):
        self.root = config.root_directory
        if not self.root.exists():
            self.root.mkdir(parents=True, exist_ok=True)

    @typechecked
    def list_files(self, path: Path = Path("."), pattern: str = "*", recursive: bool = False) -> List[Path]:
        # Ensure the path is treated as relative to the root, even if an absolute path is mistakenly provided
        if path.is_absolute():
            path = path.relative_to(self.root)

        search_path = Path(self.root, path)

        if search_path.is_file():
            return [path]

        search_pattern = str(
            search_path / "**" / pattern) if recursive else str(search_path / pattern)

        return [Path(p).relative_to(self.root) for p in glob.glob(search_pattern, recursive=recursive) if Path(p).is_file()]

    @typechecked
    def create_file(self, path: Path, data: str):
        full_path = Path(self.root, path)

        # Check that the file does not already exist.
        if full_path.exists():
            raise FileExistsError(f"File already exists: {path}")

        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w") as file:
            file.write(data)

    @typechecked
    def update_file(self, path: Path, data: str):
        full_path = Path(self.root, path)

        # Check that the file exists.
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(full_path, "w") as file:
            file.write(data)

    @typechecked
    def read_file(self, path: Path) -> str:
        full_path = Path(self.root, path)

        # Check that the file exists.
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(full_path, "r") as file:
            return file.read()

    @typechecked
    def delete_file(self, path: Path, pattern: str = "*", recursive: bool = False):
        deleted_files = False

        for file_path in self.list_files(path, pattern, recursive):
            full_path = Path(self.root, file_path)
            os.remove(full_path)
            deleted_files = True

        # After deleting files, check and remove any empty directories
        if deleted_files and recursive:
            # Walking through the directory tree from the bottom up to safely remove any empty directories
            for dirpath, dirnames, filenames in os.walk(Path(self.root, path), topdown=False):
                # Convert dirpath to Path object for consistency with Pathlib usage
                dirpath = Path(dirpath)
                if dirpath == self.root:
                    # Prevent attempting to remove the root directory
                    break
                dirpath.rmdir()
        elif deleted_files:
            # Attempt to remove the parent directory if not recursive and it's empty, avoiding the root
            parent_dir = Path(self.root, path).parent
            if parent_dir != self.root:
                parent_dir.rmdir()
