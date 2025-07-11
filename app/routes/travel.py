from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.travel import Travel
from app.database import get_session

router = APIRouter()


@router.get("/{travel_id}")
def get_user(travel_id: int, session: Session = Depends(get_session)):

    travel = session.exec(select(Travel).where(Travel.id == travel_id)).first()

    if not travel:
        return HTTPException(status_code=404, detail="Travel not found")

    return travel
