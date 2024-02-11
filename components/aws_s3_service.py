import logging

import boto3
from botocore.exceptions import ClientError

from environmemt import S3_BUCKET, AWS_SERVER_PUBLIC_KEY, AWS_SERVER_SECRET_KEY, REGION_NAME

# connect to AWS S3 via boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
    aws_secret_access_key=AWS_SERVER_SECRET_KEY,
    region_name=REGION_NAME
)


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
