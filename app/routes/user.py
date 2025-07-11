from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import uuid4

from app.models.user import User, UserPatch
from app.types.user import UserCreate, UserResponse
from app.database import get_session

router = APIRouter()


@router.post("/")
def create_user(user: UserCreate, session: Session = Depends(get_session)):

    new_user = User(**user.model_dump(), id=str(uuid4()), score=5.0)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    response = UserResponse(**new_user.model_dump())
    return response

@router.get("/", response_model=list[UserResponse])
def list_users(session: Session = Depends(get_session)):

    users = session.exec(select(User)).all()
    return [UserResponse(**user.model_dump()) for user in users]


@router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    return user


@router.patch("/{user_id}")
def update_user(user_id: int, data: UserPatch, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    user_data = data.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}
