import serializers
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import text, CursorResult
from database import engine
from utils.helper import make_sql, calc_age, formatStringToDate
from lib.auth import verify_password, get_user, create_access_token, check_token
from typing import Annotated


router = APIRouter(
    tags=['connect']
)


@router.get("/revalidate")
async def revalidate(new_token: Annotated[str, Depends(check_token)]):
    return {
        "access_token": new_token,
        "token_type": "bearer"
    }


@router.post("/connect")
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

    # update user age if one yaer is passed
    await update_age(user)

    return {
        "access_token": create_access_token(user, form_data.expire),
        "token_type": "bearer"
    }


async def update_age(user: dict[serializers.UserOut, None]):
    items = user.copy()
    items["age"] = calc_age(formatStringToDate(items["birthday_date"]))
    q, values = make_sql(
        "UPDATE",
        table="users",
        items=items,
        fields=["age"],
        id=items["id"]
    )
    with engine.begin() as conn:
        result: CursorResult = conn.execute(text(q), values)
        if result.rowcount == 0:
            print("Error date and age")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
