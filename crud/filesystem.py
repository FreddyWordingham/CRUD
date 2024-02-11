from pathlib import Path

from typeguard import typechecked

from .storage import Storage


class FileSystemStorage(Storage):
    @typechecked
    def __init__(self, root: Path):
        self.root = root

        # Ensure the root directory exists
        self.root.mkdir(parents=True, exist_ok=True)

    @typechecked
    def list_files(self, directory: Path, pattern: str = "*.*"):

        pass

    @typechecked
    def create_file(self, local_file_path: Path, destination_file_path: Path):
        pass

    @typechecked
    def read_file(self, local_file_path: Path, destination_file_path: Path):
        pass

    @typechecked
    def delete_file(self, destination_file_path: Path):
        pass
