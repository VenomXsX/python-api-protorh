from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Json, NaiveDatetime
from typing import List, Optional, Union
from datetime import date
from sqlalchemy import CursorResult, RowMapping


Base = declarative_base()


class User(BaseModel):
    id: int
    email: str
    password: str
    firstname: str
    lastname: str
    birthday_date: NaiveDatetime
    address: str
    postal_code: str
    age: int
    meta: str
    registration_date: NaiveDatetime
    token: str
    role: str



class CreateUser(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    birthday_date: NaiveDatetime
    address: str
    postal_code: str
    age: int
    meta: str
    registration_date: NaiveDatetime
    token: str
    role: str


class UpdateUser(BaseModel):
    email: Optional[str]
    password: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    birthday_date: Optional[NaiveDatetime]
    address: Optional[str]
    postal_code: Optional[str]
    age: Optional[int]
    meta: Optional[str]
    registration_date: Optional[NaiveDatetime]
    token: Optional[str]
    role: Optional[str]


class RequestRH(BaseModel):
    id: int
    user_id: int
    content: str
    registration_date: NaiveDatetime
    visibility: bool
    close: bool
    last_action: NaiveDatetime
    content_history: List[Json]


class Event(BaseModel):
    id: int
    name: str
    date: date
    description: str
    user_id: int
    department_id: int


class EventRequired(BaseModel):
    name: str
    date: str
    description: str
    user_id: int
    department_id: int


class EventOptional(BaseModel):
    name: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None
    department_id: Optional[int] = None


class Department(BaseModel):
    id: int
    name: str
