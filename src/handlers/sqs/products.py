import json
import os
import io

from PIL import Image

from common import s3
from common.constants import S3
from models.product import find_product_by_store, update_product


def handler(event: dict, _):
    records = event["Records"]

    for record in records:
        body = json.loads(record["body"])
        object_key = body["object_key"]
        store_slug = body["store_slug"]
        product_id = body["product_id"]
        file_type = body["file_type"]

        response = s3.get_object(os.environ.get("ZAPBUY_BUCKET_NAME"), object_key)
        original_image = Image.open(io.BytesIO(response["Body"].read()))

        sizes = {"400x400": (400, 400), "150x150": (150, 150)}
        for name, size in sizes.items():
            buffer = io.BytesIO()
            resized_image = original_image.resize(size)
            resized_image.save(buffer, format=file_type.upper(), quality=85)
            buffer.seek(0)

            s3.put_object(
                os.environ.get("ZAPBUY_IMAGES_BUCKET_NAME"),
                f"{store_slug}/{product_id}-{name}.{file_type}",
                f"image/{file_type}",
                buffer
            )

        product = find_product_by_store(product_id, store_slug)
        product["image_url"] = S3.ZAPBUY_BUCKET_URI + f"/{store_slug}/{product_id}.{file_type}"
        product["image_150x150_url"] = S3.ZAPBUY_BUCKET_IMAGES_URI + f"/{store_slug}/{product_id}-150x150.{file_type}"
        product["image_400x400_url"] = S3.ZAPBUY_BUCKET_IMAGES_URI + f"/{store_slug}/{product_id}-400x400.{file_type}"

        update_product(product)

    return {"status_code": 200, "body": "Image successfully resized"}
