import boto3
import botocore
import os


class S3:
    def __init__(self):
        self.s3 = boto3.resource("s3")

    def is_exists(self, bucket: str, key: str) -> bool:
        try:
            self.s3 = boto3.resource("s3")
            self.s3.Object(bucket, key).load()
        except botocore.exceptions.ClientError as e:
            return False
        else:
            return True

    def download_directory(self, bucket: str, key: str, dst: str) -> None:
        bucket_obj = self.s3.Bucket(bucket)
        for obj in bucket_obj.objects.filter(Prefix=key):
            local_path = os.path.join(dst, os.path.dirname(obj.key))
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            filepath = os.path.join(local_path, os.path.basename(obj.key))
            bucket_obj.download_file(obj.key, filepath)
