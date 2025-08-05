import base64
import hashlib
import hmac
import json
import os
from typing import Any, Dict, Optional

import boto3
import requests
from botocore.exceptions import ClientError
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode

from app.models.user import User
from app.types.auth import JWKS, JWTAuthCredentials
from app.types.user import UserCreate


def get_auth_error_message() -> str:
    return "Autentication failed."


def get_auth_secrets() -> Dict[str, str]:
    secret_name = os.getenv("AWS_COGNITO_SECRET_NAME")
    region_name = os.getenv("AWS_DEFAULT_REGION")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name,
        )

    except ClientError as e:
        raise e

    return json.loads(get_secret_value_response["SecretString"])


def create_user_cognito(user: UserCreate, db_user: User):
    cognito_client = boto3.client("cognito-idp")
    try:
        cognito_client.admin_create_user(
            UserPoolId=get_auth_secrets()["user_pool_id"],
            Username=user.email,
            UserAttributes=[
                {
                    "Name": "phone_number",
                    "Value": user.phone,
                },
                {
                    "Name": "email",
                    "Value": user.email,
                },
                {
                    "Name": "given_name",
                    "Value": user.name,
                },
            ],
            ValidationData=[
                {
                    "Name": "email",
                    "Value": user.email,
                },
            ],
            MessageAction="SUPPRESS",
            DesiredDeliveryMediums=["EMAIL"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def calc_secret(username: str):
    secrets = get_auth_secrets()
    key = bytes(secrets["client_secret"], "utf-8")
    msg = bytes(username + secrets["client_id"], "utf-8")

    new_digest = hmac.new(key, msg, hashlib.sha256).digest()
    secret_hash = base64.b64encode(new_digest).decode()

    return secret_hash


def get_jwks():
    try:
        response = requests.get(get_auth_secrets()["jwks_url"])
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=500,
            detail=get_auth_error_message(),
        )


def get_public_key(token: str, jwks: JWKS) -> Optional[Dict[str, str]]:
    try:
        headers = jwt.get_unverified_header(token)
    except JOSEError:
        raise HTTPException(
            status_code=500,
            detail=get_auth_error_message(),
        )

    kid = headers.get("kid")
    if not kid:
        raise HTTPException(
            status_code=400,
            detail=get_auth_error_message(),
        )

    for key in jwks.get("keys", []):
        if key["kid"] == kid:
            return key

    raise HTTPException(
        status_code=403,
        detail=get_auth_error_message(),
    )


def verify_jwt(token: str, jwks: Dict[str, Any]):
    pub_key = get_public_key(token, jwks)

    if not pub_key:
        raise HTTPException(
            status_code=403,
            detail=get_auth_error_message(),
        )

    pub_key = jwk.construct(get_public_key(token, jwks))
    message, encoded_signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode())

    return pub_key.verify(message.encode(), decoded_signature)


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    def verify_token(self, jwt_credentials: JWTAuthCredentials) -> bool:
        try:
            public_key = self.kid_to_jwk[jwt_credentials.header["kid"]]
        except KeyError:
            raise HTTPException(
                status_code=403,
                detail=get_auth_error_message(),
            )

        key = jwk.construct(public_key)
        decoded_signature = base64url_decode(jwt_credentials.sig.encode())

        return key.verify(jwt_credentials.message.encode(), decoded_signature)

    async def __call__(self, request: Request) -> Optional[JWTAuthCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request,
        )

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail=get_auth_error_message(),
                )

            jwt_token = credentials.credentials
            message, signature = jwt_token.rsplit(".", 1)

            try:
                jwt_credentials = JWTAuthCredentials(
                    jwt_token=jwt_token,
                    header=jwt.get_unverified_claims(jwt_token),
                    claims=jwt.get_unverified_claims(jwt_token),
                    sig=signature,
                    message=message,
                )
            except JWTError:
                raise HTTPException(
                    status_code=403,
                    detail=get_auth_error_message(),
                )

            if not self.verify_token(jwt_credentials=jwt_credentials):
                raise HTTPException(
                    status_code=403,
                    detail=get_auth_error_message(),
                )

            return jwt_credentials


auth_bearer = AuthBearer()
