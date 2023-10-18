from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional, List
import serializers
from database import SessionLocal
from models import User, RequestRH, Event, Department


app = FastAPI()

db = SessionLocal()

@app.get("/events", response_model=List[serializers.Event])
def GetAllEvent():
    events = db.query(Event).all()
    return events
