import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional, List
from database import SessionLocal
from models import User, RequestRH, Event, Department
import serializers
import sys

# routers
from endpoint import event_queries
from endpoint import user_queries

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 4242

app = FastAPI()
db = SessionLocal()

app.include_router(event_queries.router)
app.include_router(user_queries.router)


@app.get("/")
def root():
    return "REST API is working yey"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
