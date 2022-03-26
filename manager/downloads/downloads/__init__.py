from logging import Logger

import injector

from downloads.application.queries import (
    FileDto,
    GetDownloadStatus,
    GetFileStatus,
    GetBulkFileStatus,
)
from downloads.application.repositories import FilesRepository, DownloadRepository
from downloads.application.use_cases import (
    FileDownload,
    FileRetry,
    FileRetryAll,
    TaskDownloadFile,
)
from downloads.domain import settings as DownloadSettings
from downloads.domain.value_objects import HashId, FailTypes

__all__ = [
    # module
    "Downloads",
    "DownloadSettings",
    # value objects
    "HashId",
    "FailTypes",
    # repositories
    "FilesRepository",
    "DownloadRepository",
    # use cases
    "FileDownload",
    "FileRetry",
    "FileRetryAll",
    "TaskDownloadFile",
    # queries
    "GetDownloadStatus",
    "GetFileStatus",
    "GetBulkFileStatus",
    # queries dtos
    "FileDto",
]


class Downloads(injector.Module):
    @injector.provider
    def file_download_uc(self, repo: FilesRepository) -> FileDownload:
        return FileDownload(repo)

    @injector.provider
    def file_retry_uc(self, repo: FilesRepository) -> FileRetry:
        return FileRetry(repo)

    @injector.provider
    def file_retry_all_uc(self, repo: FilesRepository) -> FileRetryAll:
        return FileRetryAll(repo)

    @injector.provider
    def task_download_file_uc(
        self,
        files_repo: FilesRepository,
        downloader_repo: DownloadRepository,
        logger: Logger,
    ) -> TaskDownloadFile:
        return TaskDownloadFile(
            files_repo=files_repo,
            downloader_repo=downloader_repo,
            logger=logger,
        )
