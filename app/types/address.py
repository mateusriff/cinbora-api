from datetime import datetime
from pydantic import BaseModel, Field

class Address(BaseModel):

    id: str = Field(..., title="Address ID", description="Unique identifier for the address")
    origin_address: str = Field(..., title="Origin Address", description="The starting address for the route")
    destination_address: str = Field(..., title="Destination Address", description="The ending address for the route")
    origin_lat: float = Field(None, title="Origin Latitude", description="Latitude of the origin address")
    origin_lng: float = Field(None, title="Origin Longitude", description="Longitude of the origin address")
    destination_lat: float = Field(None, title="Destination Latitude", description="Latitude of the destination address")
    destination_lng: float = Field(None, title="Destination Longitude", description="Longitude of the destination address")
    created_at: datetime = Field(default_factory=datetime.now, title="Creation Timestamp", description="Timestamp when the address was created")

class AddressCreate(BaseModel):

    origin_address: str = Field(..., title="Origin Address", description="The starting address for the route")
    destination_address: str = Field(..., title="Destination Address", description="The ending address for the route")

class AddressResponse(Address):

    id: str
    origin_address: str
    destination_address: str
    origin_lat: float
    origin_lng: float
    destination_lat: float
    destination_lng: float
    created_at: datetime
