from sqlmodel import SQLModel, Field
from typing import Union
from datetime import datetime


class User(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    email: str = Field()
    phone: str = Field()
    photo: Union[str, None] = Field(default=None)
    gender: str = Field()
    score: float
    created_at: datetime = Field(default_factory=datetime.now)


class UserPatch(SQLModel):

    name: Union[str, None] = None
    email: Union[str, None] = None
    phone: Union[str, None] = None
    photo: Union[str, None] = None
    gender: Union[str, None] = None
