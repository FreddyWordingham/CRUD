from typing import Union

from .storage_interface import StorageInterface

from .local_storage import LocalStorage
from .s3_storage import S3Storage


class StorageTypes:
    LOCAL = "local"
    S3 = "s3"


def storage(type: StorageTypes, **kwargs) -> Union[LocalStorage, S3Storage]:
    """
    Factory function to get the specified storage type instance.

    Args:
        type (str): The type of storage to initialize ("local" or "s3").
        **kwargs: Additional arguments required to initialize the storage instance.

    Returns:
        Union[LocalStorage, S3Storage]: An instance of the requested storage type.

    Raises:
        ValueError: If an unknown storage type is requested.
    """

    match type:
        case StorageTypes.LOCAL:
            return LocalStorage(**kwargs)
        case StorageTypes.S3:
            return S3Storage(**kwargs)
        case _:
            raise ValueError(f"Unknown storage type: {type}")


# Example usage:
# store = storage("local", root="./output")
# store = storage("s3", bucket_name="my-bucket-name")
