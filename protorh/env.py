from dotenv import load_dotenv
import os

load_dotenv("protorh/protorh.env")
DB_USER = os.environ["DATABASE_USER"]
DB_PASSWORD = os.environ["DATABASE_PASSWORD"]
DB_HOST = os.environ["DATABASE_HOST"]
DB_PORT = os.environ["DATABASE_PORT"]
DB_NAME = os.environ["DATABASE_NAME"]
SECRET_KEY = os.environ["SECRET_KEY"]
SALT = os.environ["SALT"]

DB_URL = "postgresql://" + DB_USER + ":" + DB_PASSWORD + \
    "@" + DB_HOST + ":" + DB_PORT + "/" + DB_NAME
