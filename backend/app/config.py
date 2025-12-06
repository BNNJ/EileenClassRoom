"""Application configuration using Pydantic Settings (supports *_FILE)."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote_plus

from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings


def read_secret_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8").strip()


def read_env_or_env_file(var_name: str) -> str | None:
    """
    Read VAR_NAME from env; if missing, read file pointed by VAR_NAME_FILE.
    """
    env_value = os.getenv(var_name)
    if env_value is not None and env_value != "":
        return env_value

    secret_file_path = os.getenv(f"{var_name}_FILE")
    if secret_file_path:
        return read_secret_file(secret_file_path)

    return None


class Settings(BaseSettings):
    # --- Database: either provide DATABASE_URL(_FILE) or components below ---
    DATABASE_URL: str | None = None  # or DATABASE_URL_FILE

    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None  # or DB_PASSWORD_FILE

    SQLALCHEMY_DRIVER: str = "postgresql+psycopg"

    # --- Security ---
    SECRET_KEY: str | None = None  # or SECRET_KEY_FILE
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- CORS ---
    FRONTEND_URL: str = "http://localhost:5173"

    # --- Environment ---
    ENVIRONMENT: str = "development"

    @model_validator(mode="after")
    def load_file_secrets_and_build_database_url(self) -> "Settings":
        # 1) Fill SECRET_KEY from SECRET_KEY_FILE if needed
        if not self.SECRET_KEY:
            loaded_secret_key = read_env_or_env_file("SECRET_KEY")
            if loaded_secret_key:
                self.SECRET_KEY = loaded_secret_key

        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY (or SECRET_KEY_FILE) must be set")

        # 2) Fill DB_PASSWORD from DB_PASSWORD_FILE if needed
        if not self.DB_PASSWORD:
            loaded_password = read_env_or_env_file("DB_PASSWORD")
            if loaded_password:
                self.DB_PASSWORD = loaded_password

        # 3) Fill DATABASE_URL from DATABASE_URL_FILE if needed
        if not self.DATABASE_URL:
            loaded_database_url = read_env_or_env_file("DATABASE_URL")
            if loaded_database_url:
                self.DATABASE_URL = loaded_database_url

        # 4) If DATABASE_URL still missing, build it from components
        if not self.DATABASE_URL:
            if not (self.DB_NAME and self.DB_USER and self.DB_PASSWORD):
                raise ValueError(
                    "Set DATABASE_URL(_FILE) or set DB_NAME, DB_USER and DB_PASSWORD(_FILE)."
                )

            encoded_password = quote_plus(self.DB_PASSWORD)
            self.DATABASE_URL = (
                f"{self.SQLALCHEMY_DRIVER}://{self.DB_USER}:{encoded_password}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )

        return self

    model_config = ConfigDict(case_sensitive=True)


settings = Settings()
