from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool


class StatusDTO(BaseModel):
    downloads: int


class DownloadDTOIn(BaseModel):
    name: str
    path: str
    url: str
    headers: Optional[Dict[str, str]] = {}


class DownloadDTOOut(BaseModel):
    hash: str
    name: str
    path: str
    url: str
    failed: int
    retries: int
    completed: bool
    creation_date: datetime
    completion_date: Optional[datetime]
    headers: Optional[Dict[str, str]]


class DownloadStatusDTO(BaseModel):
    files: Dict[int, DownloadDTOOut]
