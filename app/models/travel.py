from typing import Optional, List
from sqlmodel import Field, Column, JSON, String
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from app.types.travel import Location


from app.models.base import BaseModel


class Travel(BaseModel, table=True):
    id: str = Field(default=None, primary_key=True)
    id_driver: str = Field(foreign_key="user.id")

    origin: Location = Field(default_factory=dict, sa_column=Column(JSON))
    destination: Location = Field(default_factory=dict, sa_column=Column(JSON))
    days_of_week: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    price: float = Field()
    available_seats: int = Field()
    status: str
    description: str = Field()
    start_time: datetime = Field()
    created_at: datetime = Field(default_factory=datetime.now)


