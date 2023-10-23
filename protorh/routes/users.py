from database import SessionLocal
from typing import Optional, List, Union
import serializers
from models import User, RequestRH, Event, Department
from fastapi import APIRouter, Body
from sqlalchemy import text, CursorResult, RowMapping
from models import User
from database import engine
import json
from utils import helper

router = APIRouter(
    prefix='/users',
    tags=['user']
)

db = SessionLocal()

# get all users
@router.get("/", response_model=Union[List[serializers.User], str])
async def get_all():
    q = text("SELECT * FROM users")
    with engine.begin() as conn:
        result: RowMapping = conn.execute(q).mappings().all()
        if len(result) == 0:
            return "There is no user in the table"
    return result

# get user by id
@router.get("/{id}", response_model=Union[serializers.User, str])
async def get(id):
    q = text("SELECT * FROM users WHERE id = :id")
    values = {"id": id}
    with engine.begin() as conn:
        result: RowMapping = conn.execute(q, values).mappings().all()
        if len(result) == 0:
            return f"User id {id} doesn't exist"
    return result[0]

# add a new user
@router.post("/add", response_model=Union[serializers.CreateUser, str])
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

# delete user by id
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

# update a specific user column(s)
@router.put("/update/{id}")
async def update(id, user : serializers.UpdateUser):
    set_string, values = helper.make_fields(
        user, fields_name=["email", "password", "firstname", "lastname", "birthday_date", "address", "postal_code", "age", "meta", "registration_date", "token", "role"], id=id)

    q = text(helper.trim(f"UPDATE users SET {set_string} WHERE id = :id"))
    with engine.begin() as conn:
        result: CursorResult = conn.execute(q, values)
    if result.rowcount == 0:
        return helper.response(400, "Nothing updated, please double check the id", data=values, res=result)
    return helper.response(200, "Successfully updated, id: " + id, data=values, res=result)

# update password for specific user
@router.put("/update/password/{id}")
async def update_password(id: int, content: serializers.UpdatePasswordUser):
    q = text("UPDATE users SET password = :password WHERE id = :id")
    values = {
        "password" : content.password,
        "id": id
    }
    with engine.begin() as conn:
        result: CursorResult = conn.execute(q, values)
        if result.rowcount == 0:
            return "Something went wrong and 0 rows affected"
    return f"User id {id}'s password has been updated"


# update profile picture for specific user
@router.put("/update/profile-picture/")
async def upload_profile_picture(data: serializers.UploadProfilePictureData):
    with engine.begin() as conn:
        result: RowMapping = conn.execute(text(f"SELECT meta FROM users WHERE id = {data.id}")).mappings().all()
        meta = result[0].meta
        meta["profile_picture"] = data.url
        q = text("UPDATE users SET meta = :meta WHERE id = :id")
        values = {
            "meta": json.dumps(meta),
            "id": data.id
        }
        result: CursorResult = conn.execute(q, values)
        if result.rowcount == 0:
            return "Something went wrong and 0 rows affected"
    return f"User id {data.id}'s profile picture has been updated"
        