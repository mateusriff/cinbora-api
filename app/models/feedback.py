from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

from app.models.base import BaseModel

class Feedback(BaseModel, table=True):

    id: str = Field(default=None, primary_key=True)
    id_driver: str
    id_passenger: str
    id_travel: str
    score: Optional[float] = Field(default=None)
    comment: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class FeedbackPatch(BaseModel):

    score: Optional[float] = Field(default=None)
    comment: Optional[str] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.now)