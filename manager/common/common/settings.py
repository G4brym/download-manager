import os
from typing import Optional

from pydantic import BaseSettings

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)

ENV = os.environ.get("ENVIRONMENT", "DEV").upper()
IS_DEV = ENV == "DEV"
IS_PROD = ENV == "PROD"

BASE_SETTINGS_KWARGS = dict(
    _env_file_encoding="utf-8",
)

if IS_DEV:
    BASE_SETTINGS_KWARGS["_env_file"] = os.path.join(BASE_PATH, ".env")


class Settings(BaseSettings):
    SENTRY_DSN: Optional[str]
    DATABASE_PATH: Optional[str] = os.path.join(BASE_PATH, "db.sqlite3")


__all__ = ["CommonSettings", "BASE_SETTINGS_KWARGS"]

CommonSettings = Settings(**BASE_SETTINGS_KWARGS)
