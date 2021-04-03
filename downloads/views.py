import logging
from typing import List

from fastapi import APIRouter, HTTPException

from downloads.dataclasses import StatusDTO, DownloadDTOIn, DownloadDTOOut, SuccessResponse, DownloadStatusDTO
from downloads.models import Download

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Downloads"],
)


@router.get("/status/", response_model=StatusDTO)
def api_index():
    return dict(downloads=Download.count())


@router.post("/download/", response_model=List[DownloadDTOOut])
def api_download(files: List[DownloadDTOIn]):
    result = []

    for file in files:
        download = Download.loads(file.__dict__)
        download.save()

        logger.info('Scheduled File {} for download'.format(download.name))
        result.append(Download.dumps(download))

    return result


@router.post("/download/retry/", response_model=SuccessResponse)
def download_retry_all():
    Download.retry_all()
    return dict(success=True)


@router.post("/download/<hash>/retry/", response_model=SuccessResponse, responses={404: {"description": "Not found"}})
def download_retry_single(hash: str):
    download = Download.get_by_hash(hash)
    if not download:
        raise HTTPException(404, "Item not found")

    download.failed = 0
    download.retries = 0
    download.save()

    return dict(success=True)


@router.post("/download/status/", response_model=DownloadStatusDTO)
def download_status_bulk(files: List[str]):
    downloads = Download.list_by_hash(files)

    return {
        "success": True,
        "files": {
            download.hash: Download.dumps(download)
            for download in downloads
        }
    }


@router.get("/download/<hash>/", response_model=DownloadDTOOut, responses={404: {"description": "Not found"}})
def download_status_single(hash: str):
    download = Download.get_by_hash(hash)
    if not download:
        raise HTTPException(404, "Item not found")

    return Download.dumps(download)
