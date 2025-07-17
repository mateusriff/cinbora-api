from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import uuid4

from app.models.travel import Travel, TravelPatch
from app.types.travel import TravelCreate, TravelResponse
from app.database import get_session

router = APIRouter()

@router.post("/")
def create_user(travel: TravelCreate, session: Session = Depends(get_session)):

    new_travel = Travel(**travel.model_dump(), id=str(uuid4()))
    session.add(new_travel)
    session.commit()
    session.refresh(new_travel)

    response = TravelResponse(**new_travel.model_dump())
    return response

@router.get("/", response_model=list[TravelResponse])
def list_users(session: Session = Depends(get_session)):

    travels = session.exec(select(Travel)).all()
    return [TravelResponse(**travel.model_dump()) for travel in travels]

@router.get("/{travel_id}")
def get_user(travel_id: int, session: Session = Depends(get_session)):

    travel = session.exec(select(Travel).where(Travel.id == travel_id)).first()

    if not travel:
        return HTTPException(status_code=404, detail="Travel not found")

    return travel

@router.patch("/{travel_id}")
def update_travel(travel_id: int, data: TravelPatch, session: Session = Depends(get_session)):

    travel = session.exec(select(Travel).where(Travel.id == travel_id)).first()

    if not travel:
        return HTTPException(status_code=404, detail="Travel not found")

    travel_data = data.model_dump(exclude_unset=True)

    for key, value in travel_data.items():
        setattr(travel, key, value)

    session.add(travel)
    session.commit()
    session.refresh(travel)

    return travel

@router.delete("/{travel_id}")
def delete_travel(travel_id: int, session: Session = Depends(get_session)):

    travel = session.exec(select(Travel).where(Travel.id == travel_id)).first()

    if not travel:
        return HTTPException(status_code=404, detail="Travel not found")

    session.delete(travel)
    session.commit()

    return {"message": "Travel deleted successfully"}
