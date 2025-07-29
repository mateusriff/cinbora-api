from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from uuid import uuid4
from app.database import get_session
from app.utils import geocode_address

from app.models.address import Address
from app.types.address import AddressCreate, AddressResponse, AddressUpdate

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

@router.get("/", response_model=list[AddressResponse])
async def list_addresses(session = Depends(get_session)):

    addresses = session.exec(select(Address)).all()

    return [AddressResponse(**address.model_dump()) for address in addresses]

@router.get("/{address_id}", response_model=AddressResponse)
def get_address(address_id: str, session: Session = Depends(get_session)):

    address = session.exec(select(Address).where(Address.id == address_id)).first()

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    return AddressResponse(**address.model_dump())

@router.patch("/{address_id}")
async def update_address(address_id: str, address_update: AddressUpdate, session: Session = Depends(get_session)):

    address = session.exec(select(Address).where(Address.id == address_id)).first()

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    if address_update.address:
        lat, lng = await geocode_address(address_update.address)
        address.address = address_update.address
        address.latitude = lat
        address.longitude = lng

    session.add(address)
    session.commit()
    session.refresh(address)

    response = AddressResponse(**address.model_dump())
    return response

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: str, session: Session = Depends(get_session)):

    address = session.get(Address, address_id)

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    session.delete(address)
    session.commit()

    return {"detail": "Address deleted successfully"}
