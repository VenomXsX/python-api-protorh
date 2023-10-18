# from __main__ import app
from database import SessionLocal
from typing import Optional, List
import serializers
from models import User, RequestRH, Event, Department
from fastapi import APIRouter

router = APIRouter(
    prefix='/events',
    tags=['event']
)


db = SessionLocal()


@router.get("/1", response_model=List[serializers.Event])
def GetAllEventId():
    events = db.query(Event).all()
    return events
