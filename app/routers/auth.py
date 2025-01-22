# app/routers/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserCreate
from app.core.security import Security
from app.models.user import User, UserRead
from app.database.db import SessionDep
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.crud.user import CRUDUser

router = APIRouter()


@router.post("/register", response_model=UserCreate)
async def register(user: UserCreate, db: SessionDep):
    return await CRUDUser.create_user(user, db)


@router.post("/token")
async def login_for_access_token(
    db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = Security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Security.create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(Security.get_current_user)):
    return current_user
