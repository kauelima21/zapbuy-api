import logging

import boto3

import common.constants

logging.getLogger().setLevel(logging.INFO)

resource = boto3.resource("dynamodb", region_name="sa-east-1")
__table_name = common.constants.Database.ZAPBUY_TABLE_NAME


def is_table_created(table_name: str, resource) -> bool:
    try:
        table = resource.Table(table_name)
        if table.creation_date_time:
            logging.info("Table already exists!")
            return True
    except resource.meta.client.exceptions.ResourceNotFoundException as err:
        return False


def table_schema():
    return {
        "TableName": __table_name,
        "KeySchema": [
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "gsi1",
                "KeySchema": [
                    {"AttributeName": "sk", "KeyType": "HASH"},
                    {"AttributeName": "pk", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        "BillingMode": "PAY_PER_REQUEST",
    }


def create_table() -> bool:
    if is_table_created(__table_name, resource):
        return False

    table = resource.create_table(**table_schema())

    table.meta.client.get_waiter("table_exists").wait(TableName=__table_name)

    logging.info("table {} successfully created!".format(__table_name))

    return True


if __name__ == "__main__":
    create_table()
