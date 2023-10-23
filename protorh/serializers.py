from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Json, NaiveDatetime, validator, ValidationError
from typing import List, Optional, Union, Any, Dict
from datetime import date as _date
from sqlalchemy import CursorResult, RowMapping
import json


Base = declarative_base()


class MetaModel(BaseModel):
    profile_picture: str


class User(BaseModel):
    id: int
    email: str
    password: str
    firstname: str
    lastname: str
    birthday_date: _date
    address: str
    postal_code: str
    age: int
    meta: Dict[str, Any]
    registration_date: NaiveDatetime
    token: str
    role: str

    @validator("meta")
    def validate_meta(cls, value):
        try:
            # Try to parse the dictionary as a MetaModel
            meta_model = MetaModel(**value)
            return value
        except ValidationError as e:
            # If validation fails, raise an error
            raise ValueError(f"Invalid meta: {e}")


class CreateUser(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    birthday_date: _date
    address: str
    postal_code: str
    age: int
    meta: Dict[str, Any]
    registration_date: NaiveDatetime
    token: str
    role: str

    @validator("meta")
    def validate_meta(cls, value):
        try:
            # Try to parse the dictionary as a MetaModel
            meta_model = MetaModel(**value)
            return value
        except ValidationError as e:
            # If validation fails, raise an error
            raise ValueError(f"Invalid meta: {e}")


class UpdateUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    birthday_date: Optional[_date] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    age: Optional[int] = None
    meta: Optional[Dict[str, Any]] = None
    registration_date: Optional[_date] = None
    token: Optional[str] = None
    role: Optional[str] = None

    @validator("meta")
    def validate_meta(cls, value):
        try:
            # Try to parse the dictionary as a MetaModel
            meta_model = MetaModel(**value)
            return value
        except ValidationError as e:
            # If validation fails, raise an error
            raise ValueError(f"Invalid meta: {e}")


class UpdatePasswordUser(BaseModel):
    password: str


class UploadProfilePictureData(BaseModel):
    id: int
    path: str


class RequestRH(BaseModel):
    id: int
    user_id: int
    content: str
    registration_date: _date
    visibility: bool
    close: bool
    last_action: _date
    content_history: List[dict]


class RequestRHRequired(BaseModel):
    user_id: int
    content: str
    registration_date: _date
    visibility: bool
    close: bool
    last_action: _date
    content_history: List[dict]


class RequestRHOptional(BaseModel):
    user_id: Optional[int] = None
    content: Optional[str] = None
    registration_date: Optional[_date] = None
    visibility: Optional[bool] = None
    close: Optional[bool] = None
    last_action: Optional[_date] = None
    content_history: Optional[List[dict]] = None


class Event(BaseModel):
    id: int
    name: str
    date: _date
    date: _date
    description: str
    user_id: int
    department_id: int


class EventRequired(BaseModel):
    name: str
    date: _date
    description: str
    user_id: int
    department_id: int


class EventOptional(BaseModel):
    name: Optional[str] = None
    date: Optional[_date] = None
    description: Optional[str] = None
    user_id: Optional[int] = None
    department_id: Optional[int] = None


class Department(BaseModel):
    id: int
    name: str


class TestOptional(BaseModel):
    name: Optional[str] = None
    date: Optional[_date] = None
    number: Optional[int] = None
    rjson: Optional[dict] = None
    rarray: Optional[List[dict]] = None
    opened: Optional[bool] = None
