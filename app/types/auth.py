from typing import Dict, List

from pydantic import BaseModel


class JWKS(BaseModel):
    keys: List[Dict[str, str]]


class JWTAuthCredentials(BaseModel):
    jwt_token: str
    header: Dict[str, str]
    claims: Dict[str, str]
    sig: str
    message: str
