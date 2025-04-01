from dataclasses import InitVar, dataclass

import boto3


@dataclass
class S3Connection:
    client: str
    starting_bucket: InitVar[str | None] = None

    @classmethod
    def from_auth(
        cls,
        aws_access_id: str,
        aws_secret_key: str,
        aws_session_token: str | None = None,
    ):
        return cls(
            client=boto3.client(
                "s3",
                aws_access_key_id=aws_access_id,
                aws_secret_access_key=aws_secret_key,
                aws_session_token=aws_session_token,
            ),
            starting_bucket=None,
        )

    def __post_init__(self, starting_bucket: str | None):
        self.bucket = starting_bucket

    @property
    def bucket(self):
        if not self._bucket:
            raise ValueError("Bucket not set")
        return self._bucket

    @bucket.setter
    def bucket(self, bucket: str):
        self._bucket = bucket

    def upload(self, file_path: str, object_name: str) -> None:
        """Upload a file or group of files to S3 bucket"""
        self.client.upload_fileobj(file_path, self.bucket, object_name)
