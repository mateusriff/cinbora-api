from sqlmodel import SQLModel


class BaseModel(SQLModel):
    """Base model for all SQLModel models."""

    class Config:
        from_attributes = True
