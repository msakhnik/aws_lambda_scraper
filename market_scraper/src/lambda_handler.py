import os
from aws_lambda_powertools import Logger
from scraper.reserved import ReservedScraper
from scraper.base import BaseMarketScraper
from aws_services.kinesis import OutputKinesisStream
from aws_services.s3 import S3


logger = Logger()


# TODO: extend list of categories
# TODO: Move the constant to config file
CATEGORIES     = {"women": ["dresses", "t-shirts"]}
OUTPUT_KINESIS = os.environ.get("OUTPUT_KINESIS")
# TODO: look at context
AWS_REGION     = os.environ.get("AWS_REGION")
CACHE_BUCKET = "morwin-artifacts"
LOCAL_CHROMIUM_PATH = os.environ.get("LOCAL_CHROMIUM_PATH", "/mnt/efs/local-chromium")


def prepare_cache_data() -> None:
    """
    The function checks if local-chromium exists in the /mnt/efs
    If not if tries to download the data from S3.
    """
    logger.debug("Downloading chromium")
    if os.path.exists(LOCAL_CHROMIUM_PATH):
        return None
    s3 = S3()
    logger.debug("Check that remote folder exists:")
    if not s3.is_exists(bucket=CACHE_BUCKET, key="local-chromium"):
        s3.download_directory(bucket=CACHE_BUCKET,
                              key="local-chromium",
                              dst=os.path.dirname(LOCAL_CHROMIUM_PATH))
        logger.debug("Downloading Done!!!")


@logger.inject_lambda_context
def handler(event, context):
    scraper: BaseMarketScraper = ReservedScraper()
    kinesis = OutputKinesisStream(OUTPUT_KINESIS, AWS_REGION)
    prepare_cache_data()
    for type_, categories in CATEGORIES.items():
        for category in categories:
            for item in scraper.get_sales(type_default=type_, category=category):
                # TODO: don't forget to uncomment this
                # kinesis.put(item)
                logger.debug(f"type={type_}, category={category}, {item}")
