from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union

from typeguard import typechecked


class Storage(ABC):
    @abstractmethod
    @typechecked
    def list_files(self, pattern: str = "*") -> List[Path]:
        pass

    @abstractmethod
    @typechecked
    def create_file(self, path: Path, data: Union[str, bytes, bytearray]):
        pass

    @abstractmethod
    @typechecked
    def update_file(self, path: Path, data: Union[str, bytes, bytearray]):
        pass

    @abstractmethod
    @typechecked
    def read_file(self, path: Path, binary: bool = False) -> Union[str, bytes, bytearray]:
        pass

    @abstractmethod
    @typechecked
    def delete_file(self, path: Path, pattern: str):
        pass
