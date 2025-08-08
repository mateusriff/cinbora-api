from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.database import get_session
from app.models.travel import Travel
from app.models.user import User
from app.types.auth import JWTAuthCredentials
from app.types.travel import TravelCreate, TravelPatch, TravelResponse
from app.utils.auth_utils import auth_bearer
from app.utils.utils import haversine_distance

router = APIRouter(
    dependencies=[Depends(auth_bearer)],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_travel(
    travel: TravelCreate,
    session: Session = Depends(get_session),
):

    new_travel = Travel(**travel.model_dump(), id=str(uuid4()))

    user = session.exec(select(User).where(User.id == travel.id_driver)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Driver not found")

    session.add(new_travel)
    session.commit()
    session.refresh(new_travel)

    response = TravelResponse(**new_travel.model_dump())
    return response


@router.get("/", response_model=list[dict])  # raw dict for now
def list_travels(
    origin_latitude: float,
    origin_longitude: float,
    destination_latitude: float,
    destination_longitude: float,
    radius: int,
    session: Session = Depends(get_session),
):
    if origin_latitude is None or origin_longitude is None:
        raise HTTPException(status_code=400, detail="Both origin latitude and longitude required")
    if destination_latitude is None or destination_longitude is None:
        raise HTTPException(
            status_code=400, detail="Both destination latitude and longitude required"
        )

    stmt = select(Travel, User).join(User, Travel.id_driver == User.id)
    results = session.exec(stmt).all()

    filtered_results = []
    for travel, user in results:
        if (
            haversine_distance(
                (travel.origin["longitude"], travel.origin["latitude"]),
                (origin_longitude, origin_latitude),
            )
            <= radius
            and haversine_distance(
                (travel.destination["longitude"], travel.destination["latitude"]),
                (destination_longitude, destination_latitude),
            )
            <= radius
        ):
            travel_data = travel.model_dump()  # your Travel data as dict
            travel_data["driver_name"] = user.name
            travel_data["driver_phone"] = user.phone
            filtered_results.append(travel_data)

    return filtered_results


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
