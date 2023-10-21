# from __main__ import app
from database import SessionLocal
import serializers
from models import Event
from fastapi import APIRouter
from sqlalchemy import text, CursorResult, RowMapping
from utils import helper

router = APIRouter(
    prefix='/events',
    tags=['event']
)


db = SessionLocal()


@router.get("/")
def GetEventAll():
    q = text("SELECT * FROM event")
    res: RowMapping = db.execute(q).mappings().all()
    db.commit()
    return helper.response(
        200,
        "Events found" if len(res) != 0 else "No events found",
        data=res
    )


@router.get("/{id}")
def GetEvent(id):
    q = text("SELECT * FROM event WHERE id = :id LIMIT 1")
    # useing mappings to turn it as Array
    # because it return CursorResult by default
    res: RowMapping = db.execute(q, {"id": id}).mappings().all()
    db.commit()
    if len(res) == 0:
        return helper.response(404, "No event found. id: " + id)
    return helper.response(200, "Event found. id: " + id, data=res[0])


@router.post("/create")
def Create(item: serializers.EventRequired):
    q = text(
        "INSERT INTO event"
        "(name, date, description, user_id, department_id)"
        "VALUES"
        "(:name, :date, :description, :user_id, :department_id)"
    )
    values = {
        "name": item.name,
        "date": item.date,
        "description": item.description,
        "user_id": item.user_id,
        "department_id": item.department_id,
    }
    res: CursorResult = db.execute(q, values)
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
    q = text("DELETE FROM event WHERE id = :id")
    res: CursorResult = db.execute(q, {"id": id})
    db.commit()
    if res.rowcount == 0:
        return helper.response(
            400,
            "This event does not exist, id: " + id,
            res=res
        )
    return helper.response(200, "Sucessfully deleted, id: " + id, res=res)


@router.put("/{id}")
def Update(id, item: serializers.EventOptional):
    set_string, values = helper.make_fields(
        item,
        ["name", "description", "date", "user_id", "department_id"],
        id=id
    )

    q = text(helper.trim(f"UPDATE event SET {set_string} WHERE id = :id"))
    res: CursorResult = db.execute(q, values)
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
