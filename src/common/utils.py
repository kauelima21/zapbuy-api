import re
import unicodedata

def generate_slug(str_value: str) -> str:
    transformed_str = unicodedata.normalize("NFKD", str_value)
    transformed_str = ''.join([c for c in transformed_str if not unicodedata.combining(c)])
    transformed_str = re.sub(r'[^a-z0-9\s-]', '', transformed_str.lower())
    generated_slug = "-".join(transformed_str.split(" "))

    return generated_slug
