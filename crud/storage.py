from abc import ABC, abstractmethod
from typing import List

from typeguard import typechecked


class Storage(ABC):
    @abstractmethod
    @typechecked
    def list_files(self, directory: str, pattern: str = "*.*") -> List[str]:
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    @typechecked
    def delete_file(self, directory: str, pattern: str = "*"):
        """
        Recursively delete files or directories matching the given pattern throughout
        the storage.

        Args:
            directory (str): The directory to start the recursive deletion from.
            pattern (str): The glob pattern to match files and directories against.

        Raises:
            FileNotFoundError: If no matching files or directories are found.
        """
        pass
