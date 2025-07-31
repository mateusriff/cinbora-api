from fastapi import File
from sqlmodel import SQLModel, Field
from typing import Union
from datetime import datetime

from app.models.base import BaseModel


class User(BaseModel, table=True):

    id: str = Field(default=None, primary_key=True)
    name: str = Field()
    email: str = Field()
    phone: str = Field()
    photo: str
    gender: str = Field()
    score: float
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserPatch(BaseModel):

    name: Union[str, None] = None
    email: Union[str, None] = None
    phone: Union[str, None] = None
    photo: Union[str, None] = None
    gender: Union[str, None] = None
    updated_at: datetime = Field(default_factory=datetime.now)
