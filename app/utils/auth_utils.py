import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError
from fastapi.security import OAuth2PasswordBearer


def get_auth_secrets() -> Dict[str, str]:
    secret_name = os.getenv("AWS_COGNITO_SECRET_NAME")
    region_name = os.getenv("AWS_DEFAULT_REGION")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    return get_secret_value_response['SecretString']


class AuthBearer(OAuth2PasswordBearer):
    def __init__(self):
        url = get_auth_secrets()['domain_url']
        super().__init__(tokenUrl=url)


auth_bearer = AuthBearer()
