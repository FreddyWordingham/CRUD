from pathlib import Path
from typing import List
import shutil

from typeguard import typechecked

from . import Storage


class LocalStorage(Storage):
    @typechecked
    def __init__(self, root: str):
        """
        Create a new LocalStorage instance.

        Args:
            root (str): The root directory path for the storage.

        Raises:
            FileNotFoundError: If the root directory does not already exist.
        """

        if not Path(root).exists():
            raise FileNotFoundError(f"Root directory does not exist: {root}")

        self.root = Path(root)

    @typechecked
    def list_files(self, directory: str, pattern: str = "*") -> List[str]:
        """
        List all files in a directory that match a pattern.

        Args:
            directory (str): The destination directory path to list files from.
            pattern (str, optional): The pattern to match files against. Defaults to "*.*".

        Raises:
            FileNotFoundError: If the directory does not exist.

        Returns:
            List[str]: List of file paths.
        """

        absolute_directory = self.root / directory

        if not absolute_directory.exists():
            raise FileNotFoundError(
                f"Directory does not exist: {absolute_directory}")

        return [str(file.relative_to(self.root)) for file in absolute_directory.rglob(pattern)]

    @typechecked
    def create_file(self, data: str, path: str):
        """
        Add a file to the storage.

        Args:
            data (str): File data to upload.
            path (str): Destination path for the file.

        Raises:
            FileExistsError: If the file already exists.
        """

        absolute_path = self.root / path

        if absolute_path.exists():
            raise FileExistsError(f"File already exists: {absolute_path}")

        # Ensure parent directory exists
        absolute_path.parent.mkdir(parents=True, exist_ok=True)
        absolute_path.write_text(data)

    @typechecked
    def update_file(self, data: str, path: str):
        """
        Update the contents of an existing file.

        Args:
            data (str): New file data to upload.
            path (str): Destination path of the file to update.

        Raises:
            FileNotFoundError: If the file does not exist.
        """

        absolute_path = self.root / path

        if not absolute_path.exists():
            raise FileNotFoundError(f"File does not exist: {absolute_path}")

        backup_path = absolute_path.with_suffix(
            absolute_path.suffix + ".backup")
        absolute_path.rename(backup_path)

        try:
            absolute_path.write_text(data)
        except Exception as err:
            # Restore from backup if update fails
            backup_path.rename(absolute_path)
            raise err

        backup_path.unlink()

    @typechecked
    def read_file(self, path: str) -> str:
        """
        Read a file from the storage.

        Args:
            path (str): Destination path of the file to read.

        Raises:
            FileNotFoundError: If the file does not exist.

        Returns:
            str: File data.
        """

        absolute_path = self.root / path

        if not absolute_path.exists():
            raise FileNotFoundError(f"File does not exist: {absolute_path}")

        return absolute_path.read_text()

    @typechecked
    def delete_file(self, directory: str, pattern: str = "*"):
        """
        Recursively delete files or directories matching the given pattern starting from
        the specified directory within the storage.

        Args:
            directory (str): The directory to start the recursive deletion from.
            pattern (str): The glob pattern to match files and directories against.

        Raises:
            FileNotFoundError: If the specified directory does not exist.
            FileNotFoundError: If no matching files or directories are found within the specified directory.
        """

        starting_directory = self.root / directory

        if not starting_directory.exists():
            raise FileNotFoundError(
                f"Starting directory does not exist: {starting_directory}")

        found_files_or_dirs = list(starting_directory.rglob(pattern))
        if not found_files_or_dirs:
            raise FileNotFoundError(
                f"No file or directory matches the pattern: {pattern} in directory: {directory}")

        for path in found_files_or_dirs:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
