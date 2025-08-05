import os
from typing import Any, Dict

import boto3
from fastapi import APIRouter, Depends, Form, HTTPException

from app.types.auth import JWTAuthCredentials
from app.utils.auth_utils import (
    auth_bearer,
    calc_secret,
    get_auth_error_message,
    get_auth_secrets,
)

router = APIRouter()


@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
) -> Dict[str, Any]:
    try:
        secret_hash = calc_secret(username=email)

        params = {
            "AuthFlow": "USER_PASSWORD_AUTH",
            "AuthParameters": {
                "USERNAME": email,
                "PASSWORD": password,
                "SECRET_HASH": secret_hash,
            },
            "ClientId": get_auth_secrets()["client_id"],
        }
        cognito_client = boto3.session.Session().client("cognito-idp")
        response = cognito_client.initiate_auth(**params)
    except Exception:
        return HTTPException(
            status_code=403,
            detail=get_auth_error_message(),
        )

    return response


@router.post("/logout")
def logout(claims: JWTAuthCredentials = Depends(auth_bearer)):
    try:
        access_token = claims.jwt_token
        cognito_client = boto3.session.Session().client("cognito-idp")
        _ = cognito_client.global_sign_out(AccessToken=access_token)
    except Exception:
        return HTTPException(
            status_code=500,
            detail="Could not log out.",
        )
    return {"message": "Logged out successfully"}


@router.patch("/change_password")
def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    claims: JWTAuthCredentials = Depends(auth_bearer),
):
    try:
        username = claims.claims["username"]
        secret_hash = calc_secret(username=username)
        auth_secrets = get_auth_secrets()

        params = {
            "AuthFlow": "USER_PASSWORD_AUTH",
            "AuthParameters": {
                "USERNAME": username,
                "PASSWORD": old_password,
                "SECRET_HASH": secret_hash,
            },
            "ClientId": auth_secrets["client_id"],
        }
        cognito_client = boto3.session.Session().client("cognito-idp")
        _ = cognito_client.initiate_auth(**params)
        _ = cognito_client.set_user_password(
            UserPoolId=auth_secrets["user_pool_id"],
            Username=username,
            Password=new_password,
            Permanent=True,
        )
    except Exception:
        return HTTPException(
            status_code=403,
            detail=get_auth_error_message(),
        )
    return {"message": "Password changed"}
