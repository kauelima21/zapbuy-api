import os

from models.authentication import get_new_client


def create_mock_cognito_client_pool():
    client = get_new_client()
    response = client.create_user_pool(PoolName="test-user-pool")
    user_pool_id = response["UserPool"]["Id"]
    response = client.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName="test-client",
        GenerateSecret=False
    )
    client_id = response["UserPoolClient"]["ClientId"]
    os.environ["COGNITO_CLIENT_ID"] = client_id
