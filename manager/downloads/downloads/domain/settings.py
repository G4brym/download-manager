import os
from typing import Optional

from pydantic import BaseSettings

from common.settings import BASE_SETTINGS_KWARGS, BASE_PATH


class Settings(BaseSettings):
    API_KEY: Optional[str] = "debug"
    MAX_RETRIES: Optional[int] = 5

    TMP_PATH: Optional[str] = "/tmp/downloader/"
    DOWNLOADS_PATH: Optional[str] = os.path.join(BASE_PATH, "downloads/")


__all__ = ["DownloadSettings"]

DownloadSettings = Settings(**BASE_SETTINGS_KWARGS)
