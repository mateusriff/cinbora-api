import os
import requests
import boto3
from jose import jwt
from jose.exceptions import JOSEError
from typing import Any, Dict
from fastapi import Depends, HTTPException

from app.utils.auth_utils import auth_bearer, get_auth_secrets
from app.types.user import UserCreate
from app.models.user import User


def get_jwks():
    try:
        response = requests.get(get_auth_secrets()["jwks_url"])
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=500,
            detail="Error fetching JWKS",
        )


def get_public_key(token: str, jwk: Dict[str, Any]) -> Dict[str, Any]:
    try:
        headers = jwt.get_unverified_header(token)
    except JOSEError:
        raise HTTPException(
            status_code=500,
            detail="Invalid JWK format",
        )

    kid = headers.get("kid")
    if not kid:
        raise HTTPException(
            status_code=400,
            detail="Missing 'kid' in token header",
        )

    for key in jwk["keys"]:
        if key["kid"] == kid:
            return key

    raise HTTPException(
        status_code=403,
        detail="Public key not found for the given 'kid'",
    )


async def login(token: str = Depends(auth_bearer)) -> Dict[str, Any]:
    try:
        jwks = get_jwks()
        public_key = get_public_key(token, jwks)

        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=get_auth_secrets()["client_id"],
            issuer=f"https://cognito-idp.{os.environ['AWS_DEFAULT_REGION']}.amazonaws.com/{get_auth_secrets()['user_pool_id']}",
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTClaimsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid claims",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred",
        )


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
