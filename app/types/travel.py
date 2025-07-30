from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class Location(BaseModel):
    latitude: float
    longitude: float

class Travel(BaseModel):
    """User model for the application."""

    id: str = Field(..., title="User ID", description="Unique identifier for the travel")
    id_driver: str = Field(..., title="Driver ID", description="Unique identifier for the driver")
    origin: Location = Field(..., title="Origin", description="Origin of the travel")
    destination: Location = Field(..., title="Destination", description="Destination of the travel")
    days_of_week:  Optional[List[str]] = Field(None, title="Days of Week", description="Days of week when the travel repeats")
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
    start_time: datetime = Field(..., title="Start Time", description="Time of departure")
    created_at: datetime = Field(default_factory=datetime.now)

class TravelPatch(BaseModel):
    """Model for patching travel data."""

    origin: Location = Field(None, title="Origin", description="Origin of the travel")
    destination: Location = Field(None, title="Destination", description="Destination of the travel")
    days_of_week:  Optional[List[str]] = Field(None, title="Days of Week", description="Days of week when the travel repeats")
    price: float = Field(None, title="Travel Price", description="Price of the travel")
    available_seats: int = Field(None, title="Available Seats", description="Seats available in the vehicle")
    status: str = Field(None, title="Travel Staus", description="Status of the travel(empty, full, etc)")
    start_time: datetime = Field(None, title="Start Time", description="Time of departure")
    description: str = Field(None, title="Travel Description", description="Any more details of the travel")

class TravelCreate(BaseModel):
    """Model for creating a new travel."""

    id_driver: str
    origin: Location
    destination: Location
    days_of_week:  Optional[List[str]]
    price: float
    available_seats: int = None
    status: str = None
    start_time: datetime
    description: str = None

class TravelResponse(BaseModel):
    """Response model for travel data."""

    id: str
    id_driver: str
    origin: Location
    destination: Location
    days_of_week:  Optional[List[str]]
    price: float
    available_seats: int = None
    status: str = None
    description: str = None
    start_time: datetime = None
    created_at: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
