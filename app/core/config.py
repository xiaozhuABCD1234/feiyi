# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Dict, Any


class Settings(BaseSettings):
    PROJECT_NAME: str = "Feiyi Demo"

    DATABASE_URL: str = "sqlite:///database.db"
    # JWT 配置
    SECRET_KEY: str = (
        "1c645c96c2ba8ab716a7672f7314c4351d02accf92e3c6658588732003a40fdf"  # openssl rand -hex 32
    )

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ACCESS_TOKEN_EXPIRE_DAYS: int = 180
    # # 是否开启权限验证
    # closs_verify_user_permissions = True


settings = Settings()


TORTOISE_ORM = {
    "connections": {"default": "sqlite://./data/database.db"},
    "apps": {
        "models": {
            "models": ["app.models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "Asia/Shanghai",
}

markdowns_path = r"data/markdowns"
imgs_path = r"data/imgs"
