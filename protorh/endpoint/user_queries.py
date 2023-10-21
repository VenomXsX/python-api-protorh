from database import SessionLocal
from typing import Optional, List, Union
import serializers
from models import User, RequestRH, Event, Department
from fastapi import APIRouter
from sqlalchemy import text, CursorResult, RowMapping
from models import User
from database import engine
import json

router = APIRouter(
    prefix='/api/users',
    tags=['user']
)

db = SessionLocal()


@router.get("/", response_model=Union[List[serializers.User], str])
async def get_all():
    q = text("SELECT * from users")
    with engine.begin() as conn:
        result: RowMapping = conn.execute(q).mappings().all()
        if len(result) == 0:
            return "There is no user in the table"
    return result


@router.get("/{id}", response_model=Union[serializers.User, str])
async def get(id):
    q = text("SELECT * from users WHERE id = :id")
    values = {"id": id}
    with engine.begin() as conn:
        result: RowMapping = conn.execute(q, values).mappings().all()
        if len(result) == 0:
            return f"User id {id} doesn't exist"
    return result[0]


@router.post("/create", response_model=Union[serializers.CreateUser, str])
async def add(user: serializers.CreateUser):
    q = text(
        "INSERT INTO users (email, password, firstname, lastname, birthday_date, address, postal_code, age, meta, registration_date, token, role) VALUES (:email, :password, :firstname, :lastname, :birthday_date, :address, :postal_code, :age, :meta, :registration_date, :token, :role) RETURNING *")
    values = {
        "email": user.email,
        "password": user.password,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "birthday_date": user.birthday_date,
        "address": user.address,
        "postal_code": user.postal_code,
        "age": user.age,
        "meta": json.dumps(user.meta),
        "registration_date": user.registration_date,
        "token": user.token,
        "role": user.role
    }

    with engine.begin() as conn:
        result: CursorResult = conn.execute(q, values)
        if result.rowcount == 0:
            return "Something went wrong and 0 rows affected"
    return user


@router.delete("/delete/{id}", response_model=str)
async def delete(id: int):
    q = text("DELETE FROM users WHERE id=:id")
    values = {
        "id": id
    }
    with engine.begin() as conn:
        result: CursorResult = conn.execute(q, values)
        if result.rowcount == 0:
            return "Something went wrong and 0 rows affected"
    return f"User id {id} removed from Users"


@router.put("/update/{id}", response_model=str)
async def update(id: int, user: serializers.UpdateUser):
    entry = []
    for key, val in user:
        entry.append(f"{key} = {val},")
    entry[-1] = entry[-1][:-1]
    q = text(f"UPDATE users SET {' '.join(entry)} WHERE id = {id}")
    with engine.begin() as conn:
        result: CursorResult = conn.execute(q)
        if result.rowcount == 0:
            return "Something went wrong and 0 rows affected"
    return f"User id {id} was updated (updated fields: {entry})"
