from sqlmodel import Field
from datetime import datetime

from app.models.base import BaseModel


class Travel(BaseModel, table=True):

    id: str = Field(default=None, primary_key=True)
    id_driver: str = Field(foreign_key="usuario.id")
    origin: str = Field()
    destination: str = Field()
    price: float = Field()
    available_seats: int = Field()
    status: str
    description: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
