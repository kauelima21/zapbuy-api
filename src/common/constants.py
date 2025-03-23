import os


class Database:
    ZAPBUY_TABLE_NAME = "zapbuy"


class S3:
    ZAPBUY_BUCKET_URI = f"https://{os.environ.get('ZAPBUY_BUCKET_NAME')}.s3.amazonaws.com"
    ZAPBUY_BUCKET_IMAGES_URI = f"https://{os.environ.get('ZAPBUY_IMAGES_BUCKET_NAME')}.s3.amazonaws.com"
