from fastapi import FastAPI
from app.database.db import create_db_and_tables
from app.routers import user_router

app = FastAPI()

app.include_router(user_router.router, prefix="/users", tags=["user"])
# app.include_router(auth.auth, prefix="/user/auth", tags=["auth"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
