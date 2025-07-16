from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Feedback(BaseModel):
    """Feedback model for the application."""
   
    id: str = Field(..., title="Feedback ID", description="Unique identifier for the Feedback")
    id_driver: str = Field(..., title="Driver ID", description="ID of the driver associated with the Feedback")
    id_passenger: str = Field(..., title="Passenger ID", description="ID of the passenger associated with the Feedback")
    id_travel: str = Field(..., title="Travel ID", description="ID of the travel associated with the Feedback")
    score: Optional[float] = Field(None, title="Feedback Score", description="Score of the Feedback")
    comment: Optional[str] = Field(None, title="Feedback Comment", description="Comment provided by the user")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class FeedbackPatch(BaseModel):
    """Model for patching Feedback data."""
   
    score: Optional[float] = Field(None, title="Feedback Score", description="Score of the Feedback")
    comment: Optional[str] = Field(None, title="Feedback Comment", description="Comment provided by the user")
    updated_at: datetime = Field(default_factory=datetime.now)

class FeedbackCreate(BaseModel):
    """Model for creating a new Feedback."""
   
    id_driver: str = Field(..., title="Driver ID", description="ID of the driver associated with the Feedback")
    id_passenger: str = Field(..., title="Passenger ID", description="ID of the passenger associated with the Feedback")
    id_travel: str = Field(..., title="Travel ID", description="ID of the travel associated with the Feedback")
    score: Optional[float] = Field(None, title="Feedback Score", description="Score of the Feedback")
    comment: Optional[str] = Field(None, title="Feedback Comment", description="Comment provided by the user")

class FeedbackResponse(BaseModel):
    """Response model for Feedback data."""
   
    id: str
    id_driver: str
    id_passenger: str
    id_travel: str
    score: Optional[float] = None
    comment: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
