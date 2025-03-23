import boto3


def generate_presigned_url(bucket: str, key: str, content_type: str, expiration=3600):
    s3_client = boto3.client("s3")

    return s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expiration,
    )


def put_object(bucket: str, key: str, content_type: str, object_buffer):
    s3_client = boto3.client("s3")

    return s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=object_buffer,
        ContentType=content_type,
    )


def get_object(bucket: str, key: str):
    s3_client = boto3.client("s3")

    return s3_client.get_object(Bucket=bucket, Key=key)
