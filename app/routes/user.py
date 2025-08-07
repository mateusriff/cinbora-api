from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.types.auth import JWTAuthCredentials
from app.types.user import UserCreate, UserPatch, UserResponse
from app.utils.auth_utils import auth_bearer, create_user_cognito
from app.utils.utils import delete_user_photo, format_phone_number, upload_user_photo

router = APIRouter()


@router.post("/")
async def create_user(
    name: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    gender: str = Form(None),
    file: UploadFile = File(None),
    session: Session = Depends(get_session),
):

    try:

        response_exist_user = session.exec(User).filter(User.email == email).first()

        if response_exist_user is not None:
            raise HTTPException(status_code=500, detail="Usuário já existe")

        phone = format_phone_number(phone=phone)
        user = UserCreate(
            name=name,
            password=password,
            email=email,
            phone=phone,
            gender=gender,
        )
        user_id = str(uuid4())

        url = upload_user_photo(user_id, file)

        new_user = User(**user.model_dump(), photo=url, id=user_id, score=5.0)

        username = create_user_cognito(user)

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    except Exception as error:
        print(error)
        return error

    return UserResponse(**new_user.model_dump(), username=username)


@router.get("/", response_model=list[UserResponse])
def list_users(
    claims: JWTAuthCredentials = Depends(auth_bearer),
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()
    return [
        UserResponse(**user.model_dump(), username=user.email.lower().split("@")[0])
        for user in users
    ]


@router.get("/{user_id}")
def get_user(
    user_id: str,
    claims: JWTAuthCredentials = Depends(auth_bearer),
    session: Session = Depends(get_session),
):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    return user


@router.patch("/{user_id}")
async def update_user(
    user_id: str,
    data: UserPatch = Depends(UserPatch.as_form),
    file: UploadFile = File(None),
    claims: JWTAuthCredentials = Depends(auth_bearer),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    if file is not None:
        user.photo = upload_user_photo(user_id, file)

    user.updated_at = datetime.now()
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    claims: JWTAuthCredentials = Depends(auth_bearer),
    session: Session = Depends(get_session),
):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    delete_user_photo(user_id)
    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}
