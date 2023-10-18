import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional, List
from database import SessionLocal
from models import User, RequestRH, Event, Department
import serializers
import sys


if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 4242

app = FastAPI()

db = SessionLocal()

# Test route to get all events 
@app.get("/events", response_model=List[serializers.Event])
def GetAllEvent():
    events = db.query(Event).all()
    return events


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)