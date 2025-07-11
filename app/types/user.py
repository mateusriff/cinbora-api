from datetime import datetime
from pydantic import BaseModel, Field

class User(BaseModel):
    """User model for the application."""
    
    id: str = Field(..., title="User ID", description="Unique identifier for the user")
    name: str = Field(..., title="User Name", description="Name of the user")
    email: str = Field(..., title="User Email", description="Email address of the user")
    phone: str = Field(..., title="User Phone", description="Phone number of the user")
    photo: str = Field(None, title="User Photo", description="URL of the user's photo")
    gender: str = Field(None, title="User Gender", description="Gender of the user")
    score: float = Field(None, title="User Score", description="Score of the user")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UserPatch(BaseModel):
    """Model for patching user data."""
    
    name: str = Field(None, title="User Name", description="Name of the user")
    email: str = Field(None, title="User Email", description="Email address of the user")
    phone: str = Field(None, title="User Phone", description="Phone number of the user")
    photo: str = Field(None, title="User Photo", description="URL of the user's photo")
    updated_at: datetime = Field(default_factory=datetime.now)

class UserCreate(BaseModel):
    """Model for creating a new user."""
    
    name: str
    email: str
    phone: str
    photo: str = None
    gender: str = None

class UserResponse(BaseModel):
    """Response model for user data."""
    
    id: str
    name: str
    email: str
    phone: str
    photo: str = None
    gender: str = None
    score: float = None
    created_at: datetime = None
    updated_at: datetime = None

    def __init__(self, **data):
        if "photo" in data and data["photo"] is None:
            data["photo"] = ""
        super().__init__(**data)
