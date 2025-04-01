from dataclasses import InitVar, dataclass
from functools import partial

import boto3


@dataclass
class S3Connection:
    aws_access_id: str
    aws_secret_key: str
    aws_session_token: str
    starting_bucket: InitVar[str | None] = None

    def __post_init__(self, starting_bucket: str | None):
        self._authorized_client = partial(
            boto3.client,
            aws_access_key_id=self.aws_access_id,
            aws_secret_access_key=self.aws_secret_key,
            aws_session_token=self.aws_session_token,
        )
        self.bucket = starting_bucket

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, bucket: str):
        self._bucket = bucket

    @property
    def client(self):
        """Return an authorized S3 client for a given Bucket

        If no bucket is set, raise ValueError
        """
        if not self.bucket:
            raise ValueError("Bucket not set")
        return self._authorized_client(self.bucket)

    def upload(self, file_path: str, object_name: str) -> None:
        """Upload a file or group of files to S3 bucket"""
        self.client.upload_file(file_path, self.bucket, object_name)
