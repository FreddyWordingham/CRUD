from pathlib import Path
from typing import List, Union
import fnmatch

from botocore.exceptions import ClientError
from pydantic import BaseModel
from typeguard import typechecked
import boto3

from .base import Storage


class S3StorageConfig(BaseModel):
    bucket_name: str


class S3Storage(Storage):
    @typechecked
    def __init__(self, config: S3StorageConfig):

        self.s3 = boto3.resource("s3")
        self.bucket_name = config.bucket_name
        self.bucket = self.s3.Bucket(self.bucket_name)

    @typechecked
    def list_files(self, pattern: str = "*") -> List[Path]:
        """List all files matching the given pattern."""

        files = []
        for obj in self.bucket.objects.all():
            if fnmatch.fnmatch(obj.key, pattern):
                files.append(Path(obj.key))
        return files

    @typechecked
    def create_file(self, path: Path, data: Union[str, bytes, bytearray]):

        obj = self.s3.Object(self.bucket_name, str(path))
        obj.put(Body=data)

    @typechecked
    def update_file(self, path: Path, data: Union[str, bytes, bytearray]):

        # Check if file exists.
        obj = self.s3.Object(self.bucket_name, str(path))
        try:
            obj.load()
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                raise FileNotFoundError(f"File not found: {path}")
            else:
                raise

        # S3's put method will overwrite the file if it exists.
        self.create_file(path, data)

    @typechecked
    def read_file(self, path: Path, binary: bool = False) -> Union[str, bytes, bytearray]:

        try:
            obj = self.s3.Object(self.bucket_name, str(path))
            data = obj.get()["Body"].read()
            return data if binary else data.decode("utf-8")
        except ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(f"File not found: {path}")
            else:
                raise

    @typechecked
    def delete_file(self, pattern: str):

        files_to_delete = self.list_files(pattern)
        for file_path in files_to_delete:
            obj = self.s3.Object(self.bucket_name, str(file_path))
            obj.delete()
