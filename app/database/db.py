# app/database/db.py
from sqlmodel import Session, create_engine
from ..models.User import SQLModel
from typing import Annotated,Optional
from fastapi import Depends
from app.models.User import User, UserCreate, UserUpdate

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]