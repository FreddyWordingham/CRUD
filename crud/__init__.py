from typing import Union

from .storage_interface import StorageInterface

from .local_storage import LocalStorage
from .s3_storage import S3Storage


def storage(type: str, **kwargs) -> Union[LocalStorage, S3Storage]:
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

    if type == "local":
        return LocalStorage(**kwargs)
    elif type == "s3":
        return S3Storage(**kwargs)
    else:
        raise ValueError(f"Unknown storage type: {type}")


# Example usage:
# local_storage = storage("local", root="./path/to/local/storage")
# s3_storage = storage("s3", bucket_name="my-bucket-name")
