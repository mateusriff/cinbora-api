from sqlmodel import Field, Column, JSON
from datetime import datetime
from uuid import uuid4

from app.database import get_session

from app.models.base import BaseModel

class Address(BaseModel, table=True):

    id: str = Field(default=None, primary_key=True)

    origin_address: str = Field(default=None, nullable=False)
    destination_address: str = Field(default=None, nullable=False)

    origin_lat: float = Field(default=None, nullable=False)
    origin_lng: float = Field(default=None, nullable=False)

    destination_lat: float = Field(default=None, nullable=False)
    destination_lng: float = Field(default=None, nullable=False)

    created_at: datetime = Field(default_factory=datetime.now)