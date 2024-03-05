from pathlib import Path

from crud import storage_factory, LocalStorageConfig


if __name__ == "__main__":
    config = LocalStorageConfig(
        **{
            "root_directory": Path("./tmp")
        })
    storage = storage_factory(config)

    # # List files in the store.
    # print("Files in store:")
    # for file in storage.list_files(Path("test.txt"), "*"):
    #     print(f"> {file}")

    # # Create a file in the store.
    # storage.create_file(Path("test.txt"), "Hello, World!")
    # storage.create_file(Path("test/another.txt"), "Hello, World!")
    # storage.create_file(Path("test/data.csv"), "X,y\n1,2\n3,4\n")

    # # Read a file from the store.
    # print("Reading test.txt:")
    # print(storage.read_file(Path("test.txt")))

    # # Update a file in the store.
    # storage.update_file(Path("test.txt"), "Hello, World! Updated")

    # Delete a file from the store.
    storage.delete_file(Path("."), "*", True)
