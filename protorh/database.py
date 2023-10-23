from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from env import DB_URL

engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
