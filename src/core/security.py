# src/core/security.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


SECRET_KEY = os.getenv(
    "SECRET_KEY"
)


ALGORITHM = "HS256"



def hash_password(password):

    return pwd_context.hash(
        password
    )



def verify_password(
    password,
    hashed_password
):

    return pwd_context.verify(
        password,
        hashed_password
    )



def create_token(
    user_id
):

    payload = {

        "user_id": user_id,

        "expire":
        datetime.utcnow()
        +
        timedelta(hours=24)

    }


    return jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM

    )