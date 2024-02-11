from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from typeguard import typechecked


class Storage(ABC):
    @abstractmethod
    @typechecked
    def list_files(self, directory: Path, pattern: str = "*.*") -> List[str]:
        """
        List all files in a directory that match a pattern.

        Args:
            directory (Path): The destination directory path to list files from.
            pattern (Path, optional): The pattern to match files against. Defaults to "*.*".

        Returns:
            List[str]: List of file paths.
        """
        pass

    @abstractmethod
    @typechecked
    def create_file(self, data: str, path: Path):
        """
        Add a file to the storage.

        Args:
            data (str): File data to upload.
            path (Path): Destination path for the file.
        """
        pass

    @abstractmethod
    @typechecked
    def read_file(self, destination_file_path: Path) -> str:
        """
        Read a file from the storage.

        Args:
            path (Path): Destination path of the file to download.

        Returns:
            str: File data.
        """
        pass

    @abstractmethod
    @typechecked
    def delete_file(self, path: Path):
        """
        Delete a file from the storage.

        Args:
            path (Path): Destination path of the file to delete.
        """
        pass
