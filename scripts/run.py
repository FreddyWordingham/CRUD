from pathlib import Path

from crud import init_storage


if __name__ == "__main__":
    # Set the storage path.
    this_file = Path(__file__)
    storage_path = str(this_file.parent / ".." / "output")
    print(f"Storage path: {storage_path}")

    # Create a local storage instance.
    storage = init_storage("local", root="./output")
    # local_storage = init_storage("local", root="./path/to/local/storage")
    # s3_storage = init_storage("s3", bucket_name="my-bucket-name")

    # List files in the storage.
    print("Files in storage:")
    for file in storage.list_files(storage_path):
        print(f"> {file}")

    # Read an existing file in the storage.
    file_path = "choo/*.blip"
    try:
        storage.delete_file(file_path)
    except FileNotFoundError as e:
        pass

    # List files in the storage.
    print("\n\n*UPDATED* Files in storage:")
    for file in storage.list_files(storage_path):
        print(f"> {file}")
