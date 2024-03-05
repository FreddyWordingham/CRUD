from pydantic import BaseModel
from typeguard import typechecked

from .base import Storage
from .local_storage import LocalStorageConfig, LocalStorage


@typechecked
def storage_factory(config: BaseModel) -> Storage:
    # Derive storage class name by removing "Config" suffix and access the storage class.
    storage_class_name = config.__class__.__name__.replace(
        "Config", "")
    storage_class = globals().get(storage_class_name)

    if storage_class is not None:
        # Initialise and return the storage instance using the config object.
        return storage_class(config)
    else:
        raise ValueError(
            f"No storage class found for {config.__class__.__name__}")
