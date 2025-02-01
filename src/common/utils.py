import re

from faker.decode import unidecode


def generate_slug(str_value: str) -> str:
    transformed_str = unidecode(str_value).lower()
    transformed_str = re.sub(r'[^a-z0-9\s-]', '', transformed_str)
    generated_slug = "-".join(transformed_str.split(" "))

    return generated_slug
