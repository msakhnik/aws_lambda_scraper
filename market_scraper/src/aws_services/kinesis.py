"""
The module contains class that puts records to the Kinesis Stream
"""
import boto3
import json
from aws_lambda_powertools import Logger


logger = Logger(child=True)


class OutputKinesisStream:
    def __init__(self, name: str, region: str) -> None:
        self.name: str = name
        self.region: str = region
        self.client = boto3.client("kinesis", region)

    def put(self, payload: dict) -> dict:
        """
        Method takes payload as dictionary and sends the payload to Kinesis stream
        """
        put_response = self.client.put_record(
            StreamName=self.name, Data=json.dumps(payload), PartitionKey="DefaultKey"
        )

        logger.info(f"Kinesis response: {put_response}")
        return put_response
