from datetime import datetime
from pydantic import BaseModel, Field


class Travel(BaseModel):
    """User model for the application."""

    id: str = Field(..., title="User ID", description="Unique identifier for the travel")
    id_driver: str = Field(..., title="Driver ID", description="Unique identifier for the driver")
    origin: str = Field(..., title="Origin", description="Origin of the travel")
    destination: str = Field(..., title="Destination", description="Destination of the travel")
    price: float = Field(..., title="Travel Price", description="Price of the travel")
    available_seats: int = Field(
        None, title="Available Seats", description="Seats available in the vehicle"
    )
    status: str = Field(
        None, title="Travel Staus", description="Status of the travel(empty, full, etc)"
    )
    description: str = Field(
        None, title="Travel Description", description="Any more details of the travel"
    )
    created_at: datetime = Field(default_factory=datetime.now)
