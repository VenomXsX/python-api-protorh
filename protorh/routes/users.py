from typing import List, Union, Annotated
import serializers
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import text, CursorResult, RowMapping
from database import engine
from utils.helper import make_sql, response, calc_age
from lib.auth import get_password_hash, hash_djb2, get_user, get_current_user
from env import SALT

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# get all users
@router.get("/", response_model=List[serializers.User])
async def get_all():
    q, _ = make_sql("SELECT", table="users")
    with engine.begin() as conn:
        result: RowMapping = conn.execute(text(q)).mappings().all()
    return result


@router.get("/me")
async def get_me(current_user: Annotated[serializers.UserWithPass, Depends(get_current_user)]):
    # if user["role"] != "admin":
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="wesh t'es pas autorisé"
    #     )
    return current_user


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
@router.post("/create", summary="Create new user")
async def create(items: serializers.CreateUser):
    # check if user already exist
    user = await get_user(items.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    # check password match
    if items.password != items.confirm_pass:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password does not match",
        )

    # overwrite needed fields 'cause optional
    items.password = get_password_hash(items.password)
    items.age = calc_age(items.birthday_date)
    items.meta = {}
    items.token = hash_djb2(
        items.email + items.firstname + items.lastname + SALT
    )
    items.role = "user"

    # create query
    q, values = make_sql(
        "CREATE",
        table="users",
        items=items,
        fields=[
            "email",
            "password",
            "firstname",
            "lastname",
            "birthday_date",
            "address",
            "postal_code",
            "age",
            "meta",
            "registration_date",
            "token",
            "role"
        ],
        rjson=["meta"]
    )
    with engine.begin() as conn:
        result: CursorResult = conn.execute(text(q), values)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong, please retry"
            )
    return values


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
async def update(id, items: serializers.UpdateUser):
    q, values = make_sql("UPDATE",
                         table="users",
                         id=id,
                         items=items,
                         fields=[
                             "email",
                             "password",
                             "firstname",
                             "lastname",
                             "birthday_date",
                             "address",
                             "postal_code",
                             "age",
                             "meta",
                             "registration_date",
                             "token",
                             "role"],
                         rjson=["meta"])
    with engine.begin() as conn:
        result: CursorResult = conn.execute(text(q), values)
    if result.rowcount == 0:
        return response(400, "Nothing updated, please double check the id", data=values, res=result)
    return response(200, "Successfully updated, id: " + id, data=values, res=result)


# update password for specific user
@router.put("/update/password/{id}")
async def update_password(id: int, content: serializers.UpdatePasswordUser):
    q = text("UPDATE users SET password = :password WHERE id = :id")
    values = {
        "password": content.password,
        "id": id
    }
    with engine.begin() as conn:
        result: CursorResult = conn.execute(q, values)
        if result.rowcount == 0:
            return "Something went wrong and 0 rows affected"
    return f"User id {id}'s password has been updated"


# update profile picture for specific user
# @router.put("/upload/picture/{id}")
# async def upload_profile_picture(data: serializers.UploadProfilePictureData):
#     with engine.begin() as conn:
#         result: RowMapping = conn.execute(
#             text(f"SELECT meta FROM users WHERE id = {id}")).mappings().all()
#         meta = result[0].meta
#         meta["path"] = data.path
#         q, values = make_sql("UPDATE", table="users", id=data.id, items="")
#         result: CursorResult = conn.execute(q, values)
#         if result.rowcount == 0:
#             return "Something went wrong and 0 rows affected"
#     return f"User id {data.id}'s profile picture has been updated"
