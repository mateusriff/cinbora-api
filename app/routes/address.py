from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from uuid import uuid4
from app.database import get_session
from app.utils import geocode_address

from app.models.address import Address
from app.types.address import AddressCreate, AddressResponse

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_address(address_create: AddressCreate, session: Session = Depends(get_session)):

    if not address_create.address:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Origin and destination are required")

    lat, lng = await geocode_address(address_create.address)
    
    new_address = Address(
        id=str(uuid4()),
        address=address_create.address,
        latitude=lat,
        longitude=lng,
    )

    session.add(new_address)
    session.commit()
    session.refresh(new_address)

    response = AddressResponse(**new_address.model_dump())
    return response
