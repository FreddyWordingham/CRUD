from typing import Optional

from dotenv import find_dotenv
from pydantic_settings import BaseSettings
from typeguard import typechecked


@typechecked
class Settings(BaseSettings):
    """Storage configuration."""

    storage_target: str
    storage_local_path: Optional[str]
    storage_s3_bucket: Optional[str]

    class Config:
        """Configuration for the test environment."""
        env_file = find_dotenv()
        extra = "ignore"
        env_file_encoding = "utf-8"

    # Validation
    @typechecked
    def __init__(self, **data):
        super().__init__(**data)
        self.validate()

    @typechecked
    def validate(self):
        """Validate the settings."""
        if self.storage_target not in ["local", "s3"]:
            raise ValueError(
                f"Invalid storage target '{self.storage_target}'. Must be 'local' or 's3'.")

        if self.storage_target == "local" and not self.storage_local_path:
            raise ValueError("Local storage requires a path to be specified.")
        elif self.storage_target == "s3" and not self.storage_s3_bucket:
            raise ValueError(
                "S3 storage requires a bucket name to be specified.")


SETTINGS = Settings()
