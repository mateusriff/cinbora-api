from sqlmodel import Field
from datetime import datetime

from app.models.base import BaseModel


class Travel(BaseModel, table=True):

    id: str = Field(default=None, primary_key=True)
    id_driver: str = Field(foreign_key="travel.id")
    origin: str = Field()
    destination: str = Field()
    price: float = Field()
    available_seats: int = Field()
    status: str
    description: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)

class TravelPatch(BaseModel):

    origin: str = Field(None)
    destination: str = Field(None)
    price: float = Field(None)
    available_seats: int = Field(None)
    status: str = Field(None)
    description: str = Field(None)
