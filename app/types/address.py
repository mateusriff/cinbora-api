from datetime import datetime
from pydantic import BaseModel, Field

class Address(BaseModel):

    id: str = Field(..., title="Address ID", description="Unique identifier for the address")
    address: str = Field(..., title="Address", description="The address for the route")
    latitude: float = Field(None, title="Latitude", description="Latitude of the address")
    longitude: float = Field(None, title="Longitude", description="Longitude of the address")
    created_at: datetime = Field(default_factory=datetime.now, title="Creation Timestamp", description="Timestamp when the address was created")

class AddressCreate(BaseModel):

    address: str = Field(..., title="Address", description="The address for the route")

class AddressResponse(Address):

    id: str
    address: str
    latitude: float
    longitude: float
    created_at: datetime

class AddressUpdate(BaseModel):

    address : str = Field(None, title="Address", description="The address for the route")
    updated_at: datetime = Field(default_factory=datetime.now, title="Update Timestamp", description="Timestamp when the address was last updated")