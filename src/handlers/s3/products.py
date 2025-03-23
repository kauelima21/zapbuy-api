import os
import io

from PIL import Image

from common import s3
from common.constants import S3
from models.product import find_product_by_store, update_product


def handler(event: dict, _):
    records = event["Records"]

    for record in records:
        object_key = record["s3"]["object"]["key"]
        product_keys = object_key.split("/")
        store_slug = product_keys[0]
        product_id = product_keys[1].split(".")[0]
        file_type = product_keys[1].split(".")[1]

        response = s3.get_object(os.environ.get("ZAPBUY_BUCKET_NAME"), object_key)
        original_image = Image.open(io.BytesIO(response["Body"].read()))

        sizes = {"400_400": (400, 400), "150_150": (150, 150)}
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
        product["image_150_150_url"] = S3.ZAPBUY_BUCKET_IMAGES_URI + f"/{store_slug}/{product_id}-150_150.{file_type}"
        product["image_400_400_url"] = S3.ZAPBUY_BUCKET_IMAGES_URI + f"/{store_slug}/{product_id}-400_400.{file_type}"

        update_product(product)

    return {"status_code": 200, "body": "Image successfully resized"}
