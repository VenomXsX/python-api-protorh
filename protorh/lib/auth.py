from env import SALT, SECRET_KEY
from jose import JWTError, jwt
from passlib.hash import md5_crypt
from database import engine
from utils.helper import make_sql, formatDateToString
from sqlalchemy import text, RowMapping
from typing import Union, Annotated
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import serializers


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/connect")


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
        fields=[
            "id",
            "email",
            "firstname",
            "lastname",
            "birthday_date",
            "age",
            "password",
            "role"
        ]
    )
    with engine.begin() as conn:
        res: RowMapping = conn.execute(
            text(q), values).mappings().all()
    if len(res) > 0 and res[0] is not None:
        user = dict(res[0])
        # overwrite brith date to format string
        user["birthday_date"] = formatDateToString(user["birthday_date"])
        return dict(user)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # define error
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = serializers.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user(token_data.email)
    if user is None:
        raise credentials_exception
    return serializers.UserOut(**user)


def create_access_token(data: dict, expires_delta: Union[int, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
