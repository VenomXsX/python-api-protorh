from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, BigInteger, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    email = Column(String, nullable=True)
    password = Column(String, nullable=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    birthday_date = Column(Date, nullable=True)
    address = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    age = Column(BigInteger, nullable=True)
    meta = Column(JSON, nullable=True)
    registration_date = Column(Date, server_default=func.now(), nullable=False)
    token = Column(String, nullable=True)
    role = Column(String, nullable=True)


class RequestRH(Base):
    __tablename__ = "request_rh"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    content = Column(String, nullable=True)
    registration_date = Column(Date, server_default=func.now(), nullable=False)
    visibility = Column(Boolean, nullable=True)
    close = Column(Boolean, nullable=True)
    last_action = Column(Date, onupdate=func.now(), nullable=True)
    content_history = Column(ARRAY(JSON), nullable=True)


class Event(Base):
    __tablename__ = "event"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    date = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=True)
    department_id = Column(BigInteger, ForeignKey(
        "department.id"), nullable=True)


class Department(Base):
    __tablename__ = "department"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
