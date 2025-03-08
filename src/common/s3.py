import boto3


def generate_presigned_url(bucket: str, key: str, type: str, expiration=3600):
    s3_client = boto3.client("s3")

    return s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
            "ContentType": type,
        },
        ExpiresIn=expiration,
    )
