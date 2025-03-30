import re
import unicodedata


def generate_slug(str_value: str) -> str:
    transformed_str = unicodedata.normalize("NFKD", str_value)
    transformed_str = ''.join([c for c in transformed_str if not unicodedata.combining(c)])
    transformed_str = re.sub(r'[^a-z0-9\s-]', '', transformed_str.lower())
    generated_slug = "-".join(transformed_str.split(" "))

    return generated_slug


def remove_dict_keys(item: dict | list, keys: list):
    if isinstance(item, dict):
        for key in keys:
            if key in item:
                del item[key]

    if isinstance(item, list):
        for i in item:
            for key in keys:
                if key in i:
                    del i[key]

    return item


def get_current_timestamp():
    import pytz

    from datetime import datetime

    timezone = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(timezone)

    return current_time.timestamp()
