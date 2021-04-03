from dataclasses import dataclass
from enum import Enum
from typing import Dict

from pydantic import BaseModel


class FailTypes(Enum):
    ServerError = 1
    ReachingError = 2
    LocalIOError = 3


class SuccessResponse(BaseModel):
    success: bool


class StatusDTO(BaseModel):
    downloads: int


class DownloadDTOIn(BaseModel):
    hash: str
    name: str
    path: str
    url: str
    headers: Dict[str, str]


class DownloadDTOOut(BaseModel):
    hash: str
    name: str
    path: str
    url: str
    failed: FailTypes
    retries: int
    completed: bool


class DownloadStatusDTO(BaseModel):
    files: Dict[int, DownloadDTOOut]
