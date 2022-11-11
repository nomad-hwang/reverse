from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent


class Config(BaseSettings):
    DEBUG: bool

    SECRET_KEY: str

    INITIAL_ADMIN_USERNAME: str
    INITIAL_ADMIN_PASSWORD: str

    # BACKEND_CORS_ORIGINS: list[str]

    DB_HOST: str | None
    DB_PORT: int | None
    DB_USER: str | None
    DB_PASSWORD: str | None
    DB_NAME: str | None

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        env_prefix = "BASTION_"


settings = Config()
