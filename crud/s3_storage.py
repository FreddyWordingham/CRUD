from botocore.exceptions import ClientError, NoCredentialsError
from typing import List
import boto3
import fnmatch

from typeguard import typechecked

from .base import StorageInterface
from pathlib import PurePosixPath


class S3Storage(StorageInterface):
    @typechecked
    def __init__(self, bucket_name: str):
        """
        Initialize an S3Storage instance, verifying the existence of the bucket.

        Args:
            bucket_name (str): The name of the S3 bucket to use.

        Raises:
            FileNotFoundError: If the bucket does not exist.
        """

        self.s3 = boto3.resource("s3")
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)

        if not self.bucket_exists(bucket_name):
            raise FileNotFoundError(f"Bucket does not exist: {bucket_name}")

    def bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if an S3 bucket exists.

        Args:
            bucket_name (str): The name of the bucket to check.

        Returns:
            bool: True if the bucket exists, False otherwise.
        """
        s3_client = boto3.client('s3')
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            return True
        except (ClientError, NoCredentialsError):
            return False

    @typechecked
    def list_files(self, directory: str, pattern: str = "*") -> List[str]:
        """
        List all files in a "directory" that match a pattern.

        Args:
            directory (str): The "directory" path to list files from.
            pattern (str, optional): The pattern to match files against.

        Returns:
            List[str]: List of file keys.
        """

        files = []
        for obj in self.bucket.objects.filter(Prefix=directory):
            if fnmatch.fnmatch(obj.key, pattern):
                files.append(obj.key)
        return files

    @typechecked
    def create_file(self, data: str, path: str):
        """
        Add a file to the S3 bucket.

        Args:
            data (str): File data to upload.
            path (str): S3 object key.
        """

        self.s3.Object(self.bucket.name, path).put(Body=data)

    @typechecked
    def update_file(self, data: str, path: str):
        """
        Update the contents of an existing file in S3.

        Args:
            data (str): New file data to upload.
            path (str): S3 object key.
        """

        self.create_file(data, path)

    @typechecked
    def read_file(self, path: str) -> str:
        """
        Read a file from S3.

        Args:
            path (str): S3 object key.

        Returns:
            str: File data.
        """

        try:
            obj = self.s3.Object(self.bucket.name, path)
            return obj.get()["Body"].read().decode("utf-8")
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(f"File does not exist: {path}")
            else:
                raise

    @typechecked
    def delete_file(self, directory: str, pattern: str = "*"):
        """
        Deletes files matching the given pattern starting from the specified "directory".

        Args:
            directory (str): The "directory" to start the deletion from.
            pattern (str): The glob pattern to match files against.
        """

        delete_objects = []
        for obj in self.bucket.objects.filter(Prefix=directory):
            if fnmatch.fnmatch(PurePosixPath(obj.key).name, pattern):
                delete_objects.append({"Key": obj.key})

        if delete_objects:
            self.bucket.delete_objects(Delete={"Objects": delete_objects})
