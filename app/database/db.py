# app/database/db.py
from sqlmodel import Session, create_engine
from ..models.user import SQLModel
from typing import Annotated, Optional
from fastapi import Depends

from app.models.user import User, UserCreate, UserUpdate
from app.core.config import settings

sqlite_url = settings.DATABASE_URL

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
