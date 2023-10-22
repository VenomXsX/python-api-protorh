from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import date as _date


Base = declarative_base()


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
    meta: str
    registration_date: _date
    token: str
    role: str


class CreateUser(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    birthday_date: _date
    address: str
    postal_code: str
    age: int
    meta: str
    registration_date: _date
    token: str
    role: str


class UpdateUser(BaseModel):
    email: Optional[str]
    password: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    birthday_date: Optional[_date]
    address: Optional[str]
    postal_code: Optional[str]
    age: Optional[int]
    meta: Optional[str]
    registration_date: Optional[_date]
    token: Optional[str]
    role: Optional[str]


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