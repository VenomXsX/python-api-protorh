# from __main__ import app
from database import SessionLocal
from typing import Optional, List, Union
import serializers
from models import User, RequestRH, Event, Department
from fastapi import APIRouter
from sqlalchemy import text

router = APIRouter(
    prefix='/events',
    tags=['event']
)


db = SessionLocal()


@router.get("/get_id/{event_id}", response_model=Union[serializers.Event, str])
def GetEvent(event_id):
    res = db.query(Event).get(event_id)
    if not res:
        return "No event found. id: " + event_id
    return res


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
    # with
    res = db.execute(q, values)
    db.commit()
    return (event, res)
