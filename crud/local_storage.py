from pathlib import Path
from typing import List, Union
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
    def create_file(self, path: Path, data: Union[str, bytes, bytearray]):

        full_path = Path(self.root, path)

        # Check that the file does not already exist.
        if full_path.exists():
            raise FileExistsError(f"File already exists: {path}")

        # Create the parent directory if it does not exist.
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the data to the file.
        mode = "wb" if isinstance(data, (bytes, bytearray)) else "w"
        with open(full_path, mode) as file:
            file.write(data)

    @typechecked
    def update_file(self, path: Path, data: Union[str, bytes, bytearray]):

        full_path = Path(self.root, path)

        # Check that the file exists.
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Write the data to the file.
        mode = "wb" if isinstance(data, (bytes, bytearray)) else "w"
        with open(full_path, mode) as file:
            file.write(data)

    @typechecked
    def read_file(self, path: Path, binary: bool = False) -> Union[str, bytes, bytearray]:

        full_path = Path(self.root, path)

        # Check that the file exists.
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        mode = "rb" if binary else "r"
        with open(full_path, mode) as file:
            return file.read()

    @typechecked
    def delete_file(self, path: Path, pattern: str = "*", recursive: bool = False):

        for file_path in self.list_files(path, pattern, recursive):
            full_path = Path(self.root, file_path)
            os.remove(full_path)
