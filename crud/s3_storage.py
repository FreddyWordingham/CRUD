from pathlib import Path
from typing import List
import fnmatch

from botocore.exceptions import ClientError
from pydantic import BaseModel
import boto3

from .base import Storage


class S3StorageConfig(BaseModel):
    root_directory: Path


class S3Storage(Storage):
    def __init__(self, config: S3StorageConfig):
        self.s3 = boto3.resource("s3")
        self.bucket_name = config.bucket_name
        self.bucket = self.s3.Bucket(self.bucket_name)

    def list_files(self, path: Path = Path("."), pattern: str = "*", recursive: bool = False) -> List[Path]:
        files = []
        prefix = str(path) if path != Path(".") else ""
        for obj in self.bucket.objects.filter(Prefix=prefix):
            path_obj = Path(obj.key)
            if recursive or path_obj.parent == path:
                if fnmatch.fnmatch(path_obj.name, pattern):
                    files.append(path_obj)
        return files

    def create_file(self, path: Path, data: str):
        obj = self.s3.Object(self.bucket_name, str(path))
        obj.put(Body=data)

    def update_file(self, path: Path, data: str):
        # S3's put method will overwrite the file if it exists
        self.create_file(path, data)

    def read_file(self, path: Path) -> str:
        try:
            obj = self.s3.Object(self.bucket_name, str(path))
            return obj.get()["Body"].read().decode("utf-8")
        except ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(f"File not found: {path}")
            else:
                raise

    def delete_file(self, path: Path, pattern: str = "*", recursive: bool = False):
        files_to_delete = self.list_files(path, pattern, recursive)
        for file_path in files_to_delete:
            obj = self.s3.Object(self.bucket_name, str(file_path))
            obj.delete()
