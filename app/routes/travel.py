from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from uuid import uuid4

from app.models.user import User
from app.models.travel import Travel
from app.types.travel import TravelCreate, TravelResponse, TravelPatch
from app.database import get_session

from app.utils import haversine_distance

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_travel(travel: TravelCreate, session: Session = Depends(get_session)):

    new_travel = Travel(**travel.model_dump(), id=str(uuid4()))

    user = session.exec(select(User).where(User.id == travel.id_driver)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    session.add(new_travel)
    session.commit()
    session.refresh(new_travel)

    response = TravelResponse(**new_travel.model_dump())
    return response

@router.get("/", response_model=list[TravelResponse])
def list_travels(origin_latitude: float = None, origin_longitude: float = None, destination_latitude: float = None, destination_longitude: float = None, session: Session = Depends(get_session)):

    if (origin_latitude and not origin_longitude) or (not origin_latitude and origin_longitude):
        raise HTTPException(status_code=400, detail="Both latitude and longitude required")
    elif not (origin_latitude and origin_longitude):
        travels = session.exec(select(Travel)).all()
        return [TravelResponse(**travel.model_dump()) for travel in travels]
    else:
        travels = session.exec(select(Travel)).all()

        filtered_travels = [
            travel for travel in travels
            if haversine_distance(
                (travel.origin["longitude"], travel.origin["latitude"]),
                (origin_longitude, origin_latitude)
            ) <= 3000
            and 
            haversine_distance(
                (travel.destination["longitude"], travel.destination["latitude"]),
                (destination_longitude, destination_latitude)
            ) <= 3000
        ]

        return filtered_travels
        
@router.get("/{travel_id}")
def get_travel(travel_id: str, session: Session = Depends(get_session)):

    travel = session.exec(select(Travel).where(Travel.id == travel_id)).first()

    if not travel:
        raise HTTPException(status_code=404, detail="Travel not found")

    return travel

@router.patch("/{travel_id}")
def update_travel(travel_id: str, data: TravelPatch, session: Session = Depends(get_session)):

    travel = session.exec(select(Travel).where(Travel.id == travel_id)).first()

    if not travel:
        raise HTTPException(status_code=404, detail="Travel not found")

    travel_data = data.model_dump(exclude_unset=True)

    for key, value in travel_data.items():
        setattr(travel, key, value)

    session.add(travel)
    session.commit()
    session.refresh(travel)

    return travel

@router.delete("/{travel_id}")
def delete_travel(travel_id: str, session: Session = Depends(get_session)):

    travel = session.exec(select(Travel).where(Travel.id == travel_id)).first()

    if not travel:
        raise HTTPException(status_code=404, detail="Travel not found")

    session.delete(travel)
    session.commit()

    return {"message": "Travel deleted successfully"}