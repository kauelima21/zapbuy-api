import boto3

from common.constants import Database


def get_table(table_name: str = None):
    if not table_name:
        table_name = Database.ZAPBUY_TABLE_NAME

    resource = boto3.resource("dynamodb")
    table = resource.Table(table_name)

    return table
