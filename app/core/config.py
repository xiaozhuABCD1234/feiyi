# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Demo"

    DATABASE_URL: str = "sqlite:///database.db"
    # JWT 配置
    SECRET_KEY: str = (
        "a2915205d7012894c9e9a6997d9000e15f982c52236e23fb53458ce0d00a79f5"  # openssl rand -hex 32
    )

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
