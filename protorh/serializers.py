from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Json, NaiveDatetime
from typing import List


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
    meta: Json
    registration_date: NaiveDatetime
    token: str
    role: str


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
    date: NaiveDatetime
    description: str
    user_id: int
    department_id: int

class EventIn(BaseModel):
    name: str
    date: NaiveDatetime
    description: str
    user_id: int
    department_id: int


class Department(BaseModel):
    id: int
    name: str
