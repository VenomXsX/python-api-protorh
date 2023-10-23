from env import SALT, SECRET_KEY
from jose import JWTError, jwt
from passlib.hash import md5_crypt
from database import engine
from utils.helper import make_sql, row2dict
from sqlalchemy import text, CursorResult, RowMapping, Row
from serializers import UserWithPass
from typing import Union
from datetime import datetime, timedelta
import json


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(password, hashed):
    return md5_crypt.verify(SALT + password, hashed)


def get_password_hash(password):
    return md5_crypt.hash(SALT + password)


def hash_djb2(s):
    hash = 5381
    for x in s:
        # ord(x) simply returns the unicode rep of the
        # character x
        hash = ((hash << 5) + hash) + ord(x)
    # Note to clamp the value so that the hash is
    # related to the power of 2
    return hash & 0xFFFFFFFF


async def get_user(email: str):
    q, values = make_sql(
        "SELECT",
        table="users",
        email=email,
        fields=["id", "email", "password"]
    )
    with engine.begin() as conn:
        res: RowMapping = conn.execute(
            text(q), values).mappings().all()
    if len(res) > 0 and res[0] is not None:
        user = {
            "id": res[0]["id"],
            "email": res[0]["email"],
            "password": res[0]["password"],
        }
        return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
