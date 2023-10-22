from database import SessionLocal
import serializers
from fastapi import APIRouter
from sqlalchemy import text, CursorResult, RowMapping
from utils import helper


router = APIRouter(
    prefix="/requests",
    tags=["request"]
)


db = SessionLocal()


@router.get("/")
def GetEventAll():
    q, _ = helper.make_sql("SELECT", table="request_rh")
    res: RowMapping = db.execute(text(q)).mappings().all()
    db.commit()
    return helper.response(
        200,
        "RequestRHs found" if len(res) != 0 else "No requestRHs found",
        data=res
    )


@router.get("/{id}")
def GetEvent(id):
    q, values = helper.make_sql("SELECT", table="request_rh", id=id)
    # useing mappings to turn it as Array
    # because it return CursorResult by default
    res: RowMapping = db.execute(text(q), values).mappings().all()
    db.commit()
    if len(res) == 0:
        return helper.response(404, "No requestRH found. id: " + id)
    return helper.response(200, "RequestRH found. id: " + id, data=res[0])


@router.post("/create")
def Create(items: serializers.RequestRHRequired):
    q, values = helper.make_sql(
        "CREATE",
        table="request_rh",
        items=items,
        fields=[
            "user_id",
            "content",
            "registration_date",
            "visibility",
            "close",
            "last_action",
            "content_history"
        ],
        rarray=["content_history"]
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()
    if res.rowcount == 0:
        return helper.response(
            400,
            "Oops an error occured, please retry",
            data=values,
            res=res
        )
    return helper.response(200, "Successfully addded", data=values, res=res)


@router.delete("/{id}")
def Delete(id):
    q, values = helper.make_sql(
        "DELETE",
        table="request_rh",
        id=id
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()
    if res.rowcount == 0:
        return helper.response(
            400,
            "This requestRH does not exist, id: " + id,
            res=res
        )
    return helper.response(200, "Sucessfully deleted, id: " + id, res=res)


@router.put("/{id}")
def Update(id, items: serializers.RequestRHOptional):
    q, values = helper.make_sql(
        "UPDATE",
        table="request_rh",
        id=id,
        items=items,
        fields=[
            "user_id",
            "content",
            "registration_date",
            "visibility",
            "close",
            "last_action",
            "content_history"
        ],
        rarray=["content_history"]
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()
    if res.rowcount == 0:
        return helper.response(
            400,
            "Nothing updated, please double check the id",
            data=values,
            res=res
        )

    return helper.response(
        200,
        "Successfully updated, id: " + id,
        data=values,
        res=res
    )
