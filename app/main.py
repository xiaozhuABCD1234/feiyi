from fastapi import FastAPI
from app.database.db import create_db_and_tables
from app.routers import  auth, user_router

app = FastAPI()

app.include_router(user_router.user, prefix="/users", tags=["user"])
# app.include_router(auth.auth, prefix="/user/auth", tags=["auth"])



@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", tags=["root"])
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
