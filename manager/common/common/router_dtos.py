from typing import Dict

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool


class StatusDTO(BaseModel):
    downloads: int


class DownloadDTOIn(BaseModel):
    name: str
    path: str
    url: str
    headers: Dict[str, str]


class DownloadDTOOut(BaseModel):
    hash: str
    name: str
    path: str
    url: str
    failed: int
    retries: int
    completed: bool


class DownloadStatusDTO(BaseModel):
    files: Dict[int, DownloadDTOOut]
