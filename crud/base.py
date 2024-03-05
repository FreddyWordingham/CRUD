from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from typeguard import typechecked


class Storage(ABC):
    @abstractmethod
    @typechecked
    def list_files(self, path: Path = Path("."), pattern: str = "*", recursive: bool = False) -> List[Path]:
        pass

    @abstractmethod
    @typechecked
    def create_file(self, path: Path, data: str):
        pass

    @abstractmethod
    @typechecked
    def update_file(self, path: Path, data: str):
        pass

    @abstractmethod
    @typechecked
    def read_file(self, path: Path) -> str:
        pass

    @abstractmethod
    @typechecked
    def delete_file(self, path: Path, pattern: str = "*"):
        pass
