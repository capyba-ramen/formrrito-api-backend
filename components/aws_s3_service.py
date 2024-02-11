import logging

import boto3
from botocore.exceptions import ClientError

from environmemt import S3_BUCKET

# connect to AWS S3 via boto3
s3_client = boto3.client('s3')


async def s3_upload_object(contents: bytes, content_type, object_name, bucket=S3_BUCKET):
    """Upload a file object to an S3 bucket

    :param contents: File object to upload
    :param content_type: File content type
    :param object_name: S3 object name
    :param bucket: Bucket to upload to
    :return: True if file object was uploaded, else False
    """

    try:
        response = s3_client.put_object(Body=contents, Bucket=bucket, Key=object_name,
                                        ContentType=content_type)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == "__main__":
    s3_upload_file('/Users/pinshan.chuang/Downloads/ozarks.png')
