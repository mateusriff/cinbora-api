import math
import os
from io import BytesIO

import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv("compose/.env")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
)

REGION_NAME = os.getenv("AWS_DEFAULT_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")


def format_phone_number(phone: str) -> str:
    return f"+55{phone}"


def haversine_distance(coord1, coord2):
    """
    Calculate the great-circle distance between two points
    on the Earth's surface given in decimal degrees.

    Parameters:
        coord1: tuple of float (lon1, lat1)
        coord2: tuple of float (lon2, lat2)

    Returns:
        Distance in meters as a float
    """
    # Radius of Earth in meters
    R = 6371000

    lon1, lat1 = coord1
    lon2, lat2 = coord2

    # Convert decimal degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def upload_user_photo(user_id, file):

    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Formato de imagem inválido")

    filename = f"users/user_{user_id}.png"

    try:
        contents = file.file.read()
        s3.upload_fileobj(
            Fileobj=BytesIO(contents),
            Bucket=BUCKET_NAME,
            Key=filename,
            ExtraArgs={"ContentType": file.content_type},
        )

        url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{filename}"
        return url

    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credenciais da AWS não encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")


def delete_user_photo(user_id: str):
    filename = f"users/user_{user_id}.png"

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar foto: {str(e)}")
