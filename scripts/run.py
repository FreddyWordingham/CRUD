from pathlib import Path

from crud import storage_factory, LocalStorageConfig, S3StorageConfig

from settings import SETTINGS


def init_storage():
    if SETTINGS.storage_target == "local":
        return storage_factory(LocalStorageConfig(
            **{
                "root_directory": Path(SETTINGS.storage_local_path)
            }))
    elif SETTINGS.storage_target == "s3":
        return storage_factory(S3StorageConfig(
            **{
                "bucket_name": SETTINGS.storage_s3_bucket
            }))
    else:
        raise ValueError(
            f"Invalid storage target `{SETTINGS.storage_target}`. Must be 'local' or 's3'.")


if __name__ == "__main__":
    storage = init_storage()

    # List files in the store.
    print("Files in store:")
    for file in storage.list_files("test/*"):
        print(f"> {file}")

    # # Create a file in the store.
    # storage.create_file(Path("test.txt"), "Hello, World!")
    # storage.create_file(Path("test/another.txt"), "Hello, World!")
    # storage.create_file(Path("test/data.csv"), "X,y\n1,2\n3,4\n")

    # # Read a file from the store.
    # print(storage.read_file(Path("test.txt")))

    # # Update a file in the store.
    # storage.update_file(Path("test.txt"), "Hello, World! Updated")

    # # Delete a file from the store.
    # storage.delete_file(Path("test.txt"))
