from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import User, UserPatch
from database import get_session

router = APIRouter()


@router.post("/users/")
def create_user(user: User, session: Session = Depends(get_session)):

    new_user = User(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.get("/users/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    return user


@router.patch("/user/{user_id}")
def update_user(user_id: int, data: UserPatch, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    user_data = data.dict(exclude_unset=True)

    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/user/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}
