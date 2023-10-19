# from __main__ import app
from database import SessionLocal
from typing import Optional, List, Union
import serializers
from models import User, RequestRH, Event, Department
from fastapi import APIRouter
from sqlalchemy import text, CursorResult, RowMapping
from utils import helper

router = APIRouter(
    prefix='/events',
    tags=['event']
)


db = SessionLocal()


@router.get("/", response_model=List[serializers.Event])
def GetEventAll():
    q = text("SELECT * FROM event")
    res: RowMapping = db.execute(q).mappings().all()
    db.commit()
    return res


@router.get("/{id}", response_model=Union[serializers.Event, str])
def GetEvent(id):
    q = text("SELECT * FROM event WHERE id = :id LIMIT 1")
    # useing mappings to turn it as Array
    # because it return CursorResult by default
    res: RowMapping = db.execute(q, {"id": id}).mappings().all()
    db.commit()
    if len(res) == 0:
        return "No event found. id: " + id
    return res[0]


@router.post("/create")
def Create(event: serializers.EventIn):
    q = text("INSERT INTO event (name, date, description, user_id, department_id) VALUES (:name, :date, :description, :user_id, :department_id)")
    values = {
        "name": event.name,
        "date": event.date,
        "description": event.description,
        "user_id": event.user_id,
        "department_id": event.department_id,
    }
    res: CursorResult = db.execute(q, values)
    db.commit()
    if res.rowcount == 0:
        return "Oops an error occured, please retry"
    return "Sucessfully added"


@router.delete("/{id}")
def Delete(id):
    q = text("DELETE FROM event WHERE id = :id")
    res: CursorResult = db.execute(q, {"id": id})
    db.commit()
    if res.rowcount == 0:
        return "This event does not exist, id: " + id
    return "Sucessfully deleted, id: " + id


@router.put("/{id}")
def Update(id, item: serializers.EventIn):
    set_string = ""
    if item.name:
        helper.concat_set(set_string, "name")
    if item.description:
        helper.concat_set(set_string, "description")
    if item.date:
        helper.concat_set(set_string, "date")
    if item.user_id:
        helper.concat_set(set_string, "user_id")
    if item.department_id:
        helper.concat_set(set_string, "department_id")

    q = text("UPDATE event SET " + set_string + " WHERE id = :id".strip())
    values = {
        "id": id,
        "name": item.name,
        "description": item.description,
        "date": item.date,
        "user_id": item.user_id,
        "department_id": item.department_id
    }
    res = db.execute(q, values)
    db.commit()
    return set_string
