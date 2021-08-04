import dataclasses
from typing import List

from fastapi import APIRouter, HTTPException

from common.dependencies import DependencyWrapper
from common.router_dtos import (
    StatusDTO,
    DownloadDTOIn,
    DownloadDTOOut,
    SuccessResponse,
    DownloadStatusDTO,
)
from downloads import (
    GetTotalFiles,
    FileDownload,
    FileRetry,
    GetFileStatus,
    GetBulkFileStatus,
    FileRetryAll,
)
from downloads.domain.entities import File

router = APIRouter(
    tags=["Files"],
    prefix="/files",
)


@router.get(
    "/count/",
    response_model=StatusDTO,
    summary="Get the total files downloaded (also works as an health checker)",
)
@DependencyWrapper
def file_count(get_total_files: GetTotalFiles):
    return dict(downloads=get_total_files.query())


@router.post(
    "/",
    response_model=List[DownloadDTOOut],
    summary="Create and schedule a new download",
    status_code=201,
)
@DependencyWrapper
def file_download(files: List[DownloadDTOIn], file_download_uc: FileDownload):
    response = []
    for file in files:
        _result = file_download_uc.execute(
            name=file.name,
            path=file.path,
            url=file.url,
            headers=file.headers,
        )

        if _result:
            response.append(File.to_dict(_result))

    return response


@router.get(
    "/{hash}/",
    response_model=DownloadDTOOut,
    responses={404: {"description": "Not found"}},
    summary="Get download status for a single file",
)
@DependencyWrapper
def file_status(hash: str, get_file_status: GetFileStatus):
    _result = get_file_status.query(
        hash=hash,
    )

    if not _result:
        raise HTTPException(404, "Item not found")

    return dataclasses.asdict(_result)


@router.post(
    "/{hash}/retry/",
    response_model=SuccessResponse,
    responses={404: {"description": "Not found"}},
    summary="Retry a single failed download",
    status_code=202,
)
@DependencyWrapper
def file_retry(hash: str, file_retry_uc: FileRetry):
    _result = file_retry_uc.execute(
        hash=hash,
    )

    if not _result:
        raise HTTPException(404, "Item not found")

    return dict(success=True)


@router.post(
    "/retry/",
    response_model=SuccessResponse,
    summary="Retry all failed downloads",
    status_code=202,
)
@DependencyWrapper
def file_retry_all(file_retry_all_uc: FileRetryAll):
    file_retry_all_uc.execute()

    return dict(success=True)


@router.post(
    "/status/",
    response_model=DownloadStatusDTO,
    summary="Get bulk download status for a given list of files",
)
@DependencyWrapper
def file_status_bulk(files: List[str], get_bulk_file_status: GetBulkFileStatus):
    return dict(
        files={
            file.hash: dataclasses.asdict(file)
            for file in get_bulk_file_status.query(
                hash_list=files,
            )
        }
    )
