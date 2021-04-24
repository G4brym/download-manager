import dataclasses
from typing import List

from fastapi import APIRouter, HTTPException

from common import provider
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
def file_count():
    @provider.inject
    def execute(get_total_files: GetTotalFiles):
        return get_total_files.query()

    return dict(downloads=execute())


@router.post(
    "/",
    response_model=List[DownloadDTOOut],
    summary="Create and schedule a new download",
    status_code=201,
)
def file_download(files: List[DownloadDTOIn]):
    @provider.inject
    def execute(file_download_uc: FileDownload):
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

    return execute()


@router.get(
    "/{hash}/",
    response_model=DownloadDTOOut,
    responses={404: {"description": "Not found"}},
    summary="Get download status for a single file",
)
def file_status(hash: str):
    @provider.inject
    def execute(get_file_status: GetFileStatus):
        _result = get_file_status.query(
            hash=hash,
        )

        if not _result:
            raise HTTPException(404, "Item not found")

        return dataclasses.asdict(_result)

    return execute()


@router.post(
    "/{hash}/retry/",
    response_model=SuccessResponse,
    responses={404: {"description": "Not found"}},
    summary="Retry a single failed download",
    status_code=202,
)
def file_retry(hash: str):
    @provider.inject
    def execute(file_retry_uc: FileRetry):
        _result = file_retry_uc.execute(
            hash=hash,
        )

        if not _result:
            raise HTTPException(404, "Item not found")

    execute()
    return dict(success=True)


@router.post(
    "/retry/",
    response_model=SuccessResponse,
    summary="Retry all failed downloads",
    status_code=202,
)
def file_retry_all():
    @provider.inject
    def execute(file_retry_all_uc: FileRetryAll):
        file_retry_all_uc.execute()

    execute()
    return dict(success=True)


@router.post(
    "/status/",
    response_model=DownloadStatusDTO,
    summary="Get bulk download status for a given list of files",
)
def file_status_bulk(files: List[str]):
    @provider.inject
    def execute(get_bulk_file_status: GetBulkFileStatus):
        return get_bulk_file_status.query(
            hash_list=files,
        )

    return dict(files={file.hash: file for file in execute()})
