from pathlib import Path

from crud import storage


if __name__ == "__main__":
    # Set the storage path.
    this_file = Path(__file__)
    storage_path = str(this_file.parent / ".." / "output")
    print(f"Storage path: {storage_path}")

    # Create a local storage instance.
    store = storage("local", root="./output")
    # local_storage = storage("local", root="./path/to/local/storage")
    # s3_storage = storage("s3", bucket_name="my-bucket-name")

    # List files in the store.
    print("Files in store:")
    for file in store.list_files(storage_path):
        print(f"> {file}")

    # Read an existing file in the store.
    file_path = "foo/*.bar"
    try:
        store.delete_file(file_path)
    except FileNotFoundError as e:
        pass

    # List files in the store.
    print("\n\n*UPDATED* Files in storage:")
    for file in store.list_files(storage_path):
        print(f"> {file}")
