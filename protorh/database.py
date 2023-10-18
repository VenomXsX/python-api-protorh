from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import os


load_dotenv("protorh/protorh.env")
db_user = os.environ["DATABASE_USER"]
db_password = os.environ["DATABASE_PASSWORD"]
db_host = os.environ["DATABASE_HOST"]
db_port = os.environ["DATABASE_PORT"]
db_name = os.environ["DATABASE_NAME"]

db_url = "postgresql://" + db_user + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name

engine = create_engine(db_url, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
