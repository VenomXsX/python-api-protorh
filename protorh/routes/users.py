from typing import List, Union, Annotated
import serializers
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy import text, CursorResult, RowMapping
from database import engine
from utils.helper import make_sql, response, calc_age, printer
from lib.auth import get_password_hash, hash_djb2, get_user, get_current_user, verify_password
from env import SALT
import shutil
import os

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# Endpoint : /api/user
# Type : GET
# get all users
@router.get("/", response_model=List[serializers.User])
async def get_all():
    q, _ = make_sql("SELECT", table="users")
    with engine.begin() as conn:
        result: RowMapping = conn.execute(text(q)).mappings().all()
    return result


# Endpoint : /api/user/{id_user}
# Type : GET
# get me
@router.get("/me")
async def get_me(current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    # if user["role"] != "admin":
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="wesh t'es pas autorisé"
    #     )
    return current_user


# Endpoint : /api/user/{id_user}
# Type : GET
# get user by id
@router.get("/{id}", response_model=Union[serializers.UserAdminView, serializers.UserView, str])
async def get(id, current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    q, values = make_sql("SELECT", table="users", id=id)
    with engine.begin() as conn:
        result: RowMapping = conn.execute(text(q), values).mappings().all()
        if len(result) == 0:
            return f"User id {id} doesn't exist"

    if current_user.role == "admin":
        return serializers.UserAdminView(**dict(result[0]))

    return serializers.UserView(**dict(result[0]))


# Endpoint : /api/user/create
# Type : POST
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
@router.patch("/update/{id}")
async def update(id, items: serializers.UpdateUser, current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    forbiddenFields = ["password", "token"]
    fields = [
        "email",
        "birthday_date",
        "address",
        "postal_code",
        "age",
        "meta",
        "registration_date",
    ]
    adminFields = [
        "firstname", "lastname", "role"
    ]
    items_dump = items.model_dump()
    # check forbidden
    for field in forbiddenFields:
        if items_dump[field] is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You cannot update '{field}' with this endpoint"
            )

    # check admin
    if current_user.role == "admin":
        fields.extend(adminFields)
    else:
        # check user forbidden fields
        for field in adminFields:
            if items_dump[field] is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"You cannot update: {field}"
                )

    q, values = make_sql(
        "UPDATE",
        table="users",
        id=id,
        items=items,
        fields=fields,
        rjson=["meta"]
    )
    with engine.begin() as conn:
        result: CursorResult = conn.execute(text(q), values)
    if result.rowcount == 0:
        return response(400, "Nothing updated, please double check the id", data=values, res=result)
    return response(200, "Successfully updated, id: " + id, data=values, res=result)


# update password for specific user
@router.patch("/password")
async def update_password(items: serializers.UpdatePasswordUser):

    user = await get_user(items.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password invalid E"
        )
    if not verify_password(items.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password invalid P"
        )
    if items.new_password != items.repeat_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and repeat password does not match"
        )

    items.password = get_password_hash(items.new_password)
    q, values = make_sql(
        "UPDATE",
        table="users",
        items=items,
        email=items.email,
        fields=["password"]
    )
    with engine.begin() as conn:
        result: CursorResult = conn.execute(text(q), values)
        if result.rowcount == 0:
            return "Something went wrong and 0 rows affected"
    return "User's password has been updated"


@router.post("/upload/picture/user/{id}")
async def upload_pic(id, image: UploadFile = File()):
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    # check user
    user = await get_user(id=id)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "user_error",
                "error": "User not found"
            }
        )
    # check file type
    if not image.content_type in ["image/jpeg", "image/png", "image/gif"]:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "image_type",
                "error": "Image type is not: gif, png or jpg"
            }
        )
    path = os.path.relpath("./assets/picture/profiles")
    # check if dir exist
    if not os.path.exists(path):
        os.makedirs(path)
    # save file with token as filename
    try:
        with open(f"{path}/{user['token']}.{image.filename.split('.')[-1]}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except shutil.Error as err:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "upload_error",
                "error": err
            }
        )

    return {"message": "file uploaded"}

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
