from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from typeguard import typechecked


class Storage(ABC):
    @abstractmethod
    @typechecked
    def list_files(self, directory: Path, pattern: str = "*.*") -> List[str]:
        """List all files in a directory that match a pattern.

        Args:
            directory (Path): The directory path, relative to the root of the storage, to list files from.
            pattern (Path, optional): The pattern to match files against. Defaults to "*.*".

        Returns:
            List[]: A list of file paths.
        """
        pass

    @abstractmethod
    @typechecked
    def upload(self, file_path: Path, destination: Path) -> bool:
        """Upload a file to the storage.

        Args:
            file_path (Path): Local file path to the file to upload.
            destination (Path): Destination path for the file.

        Returns:
            bool: True if the file was uploaded successfully, False otherwise.
        """
        pass

    @abstractmethod
    @typechecked
    def download(self, file_path: Path, destination: Path) -> bool:
        """Download a file from the storage.

        Args:
            file_path (Path): Path to the file to download.
            destination (Path): Local destination path for the file.

        Returns:
            bool: True if the file was downloaded successfully, False otherwise.
        """

        pass

    @abstractmethod
    @typechecked
    def delete(self, file_path: Path) -> bool:
        """Delete a file from the storage.

        Args:
            file_path (Path): Path to the file to delete.

        Returns:
            bool: True if the file was deleted successfully, False otherwise.
        """

        pass
