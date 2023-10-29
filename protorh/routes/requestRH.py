from database import engine
import serializers
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text, CursorResult, RowMapping
from utils.helper import make_sql, formatDateToString
from lib.auth import get_current_user
from typing import Annotated
from datetime import datetime


date_now = formatDateToString(datetime.utcnow())


router = APIRouter(
    prefix="/rh/msg",
    tags=["request"]
)


@router.get("/")
def get_all_rh(current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    if not current_user.role in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're not manager"
        )

    q, _ = make_sql("SELECT", table="request_rh")

    with engine.begin() as conn:
        res: RowMapping = conn.execute(text(q)).mappings().all()
        if len(res) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RH message not found"
            )

    return res


@router.get("/{id}")
def get_rh(id: int, current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    if not current_user.role in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're not manager"
        )

    q, values = make_sql("SELECT", table="request_rh", id=id)
    # using mappings to turn it as Array
    # because it return CursorResult by default
    with engine.begin() as conn:
        res: RowMapping = conn.execute(text(q), values).mappings().all()
        if len(res) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RH message not found"
            )

    return res[0]


@router.post("/add")
def add_rh(items: serializers.RequestRHInput, current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    q, _ = make_sql("SELECT", table="request_rh")
    user_id_exist = False
    with engine.begin() as conn:
        res: RowMapping = conn.execute(text(q)).mappings().all()
        for item in res:
            if item["user_id"] == items.user_id:
                user_id_exist = True

    if user_id_exist:
        q = text("SELECT * FROM request_rh WHERE user_id = :id")
        values = {
            "id": items.user_id
        }

        is_open = False
        with engine.begin() as conn:
            res: RowMapping = conn.execute(q, values).mappings().all()
            if len(res) != 0:
                for rh in res:
                    if rh["close"] != True:
                        is_open = True

        if is_open:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There is a RH message still opened, please close it before create"
            )

    # overwrite fields
    items.visibility = True
    items.close = False
    items.last_action = date_now
    items.content_history = [
        {
            "author": items.user_id,
            "content": items.content,
            "date": date_now
        }
    ]

    q, values = make_sql(
        "CREATE",
        table="request_rh",
        items=items,
        fields=[
            "user_id",
            "content",
            "visibility",
            "close",
            "last_action",
            "content_history"
        ],
        rarray=["content_history"]
    )
    with engine.begin() as conn:
        res: CursorResult = conn.execute(text(q), values)
    if res.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Oops an error occured, please retry"
        )
    return {
        "message": "Successfully addded",
        "data": values
    }


@router.post("/remove")
def close_rh(item: serializers.RequestRHId, current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    q, values = make_sql(
        "UPDATE",
        table="request_rh",
        items={
            "user_id": None,
            "close": True,
            "visibility": False,
            "last_action": date_now
        },
        fields=[
            "user_id",
            "close",
            "visibility",
            "last_action"
        ],
        id=item.id
    )
    with engine.begin() as conn:
        res: CursorResult = conn.execute(text(q), values)
        if res.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This requestRH does not exist, id: " + item.id
            )
    return {
        "message": "Sucessfully closed, id: " + str(item.id)
    }


@router.post("/update")
def Update(items: serializers.RequestRHInput, current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    q = text("SELECT id, content_history FROM request_rh WHERE user_id = :id")
    values = {
        "id": items.user_id
    }
    with engine.begin() as conn:
        res: RowMapping = conn.execute(q, values).mappings().all()
        if len(res) != 0:
            rh: serializers.RequestRHIdAndContentHistory = res[0]
            rh.content_history.append({
                "author": items.user_id,
                "content": items.content,
                "date": date_now
            })

    q, values = make_sql(
        "UPDATE",
        table="request_rh",
        id=rh["id"],
        items={
            "content": items.content,
            "last_action": date_now,
            "content_history": rh.content_history
        },
        fields=[
            "content",
            "last_action",
            "content_history"
        ],
        rarray=["content_history"]
    )
    with engine.begin() as conn:
        res: CursorResult = conn.execute(text(q), values)
    if res.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nothing updated, please double check the id",
        )

    return {
        "message": "Successfully updated, id: " + str(rh.id),
    }
