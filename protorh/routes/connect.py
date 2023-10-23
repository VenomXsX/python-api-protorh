from typing import Optional, List, Union
import serializers
from models import User, RequestRH, Event, Department
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import text, CursorResult, RowMapping
from models import User
from database import engine
import json
from utils.helper import make_sql, response, printer, calc_age
from lib.auth import get_password_hash, verify_password, hash_djb2, get_user, create_access_token
from datetime import date
from env import SALT
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix='/connect',
    tags=['connect']
)


@router.post("/")
async def connect(form_data: serializers.FormData):
    INVALID_EMAIL_OR_PASS = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )
    user = await get_user(form_data.email)
    if user is None:
        raise INVALID_EMAIL_OR_PASS

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise INVALID_EMAIL_OR_PASS

    return {
        "access_token": create_access_token(user),
        "token_type": "bearer"
    }
