from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from uuid import uuid4

from app.models.user import User, UserPatch
from app.types.user import UserCreate, UserResponse
from app.database import get_session

import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv("compose/.env")

router = APIRouter()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("REGION_NAME")
)

REGION_NAME = os.getenv("REGION_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")

@router.post("/")
async def create_user(user: UserCreate, session: Session = Depends(get_session)):

    user_id = str(uuid4())

    if user.photo_file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Formato de imagem inválido")

    filename = f"users/user_{user_id}.png"
    contents = await user.photo_file.read()

    try:
        s3.upload_fileobj(
            Fileobj=BytesIO(contents),
            Bucket=BUCKET_NAME,
            Key=filename,
            ExtraArgs={"ContentType": user.photo_file.content_type}
        )

        url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{filename}"
        #return {"message": "Upload concluído com sucesso", "url": url}

    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credenciais da AWS não encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")
    
    new_user = User(**user.model_dump(), id=user_id, score=5.0)
    new_user.photo = url

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
def get_user(user_id: str, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    return user


@router.patch("/{user_id}")
def update_user(user_id: str, data: UserPatch, session: Session = Depends(get_session)):

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
def delete_user(user_id: str, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}

#@router.post("/{user_id}/upload-photo")
async def upload_user_photo(user_id: str, file: UploadFile = File(...)):

    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Formato de imagem inválido")

    filename = f"users/user_{user_id}.png"
    contents = await file.read()

    try:
        s3.upload_fileobj(
            Fileobj=BytesIO(contents),
            Bucket=BUCKET_NAME,
            Key=filename,
            ExtraArgs={"ContentType": file.content_type}
        )

        url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{filename}"
        return {"message": "Upload concluído com sucesso", "url": url}

    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credenciais da AWS não encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

@router.delete("/{user_id}/delete-photo")
async def delete_user_photo(user_id: str):
    filename = f"users/user_{user_id}.png"

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return {"message": "Foto deletada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar foto: {str(e)}")