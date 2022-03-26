from logging import Logger

import injector

__all__ = [
    # module
    "DownloadsInfrastructure",
]

from sqlify import Sqlite3Sqlify

from downloads import (
    GetDownloadStatus,
    GetFileStatus,
    GetBulkFileStatus,
    FilesRepository,
    DownloadRepository,
)
from downloads_infrastructure.queries import (
    SqlGetDownloadStatus,
    SqlGetFileStatus,
    SqlGetBulkFileStatus,
)
from downloads_infrastructure.repositories import (
    SqlFilesRepository,
    SmartDLDownloadRepository,
)


class DownloadsInfrastructure(injector.Module):
    @injector.provider
    def get_total_files(self, database: Sqlite3Sqlify) -> GetDownloadStatus:
        return SqlGetDownloadStatus(database)

    @injector.provider
    def get_file_status(self, database: Sqlite3Sqlify) -> GetFileStatus:
        return SqlGetFileStatus(database)

    @injector.provider
    def get_bulk_file_status(self, database: Sqlite3Sqlify) -> GetBulkFileStatus:
        return SqlGetBulkFileStatus(database)

    @injector.provider
    def files_repo(self, database: Sqlite3Sqlify) -> FilesRepository:
        return SqlFilesRepository(database)

    @injector.provider
    def download_repo(self, logger: Logger) -> DownloadRepository:
        return SmartDLDownloadRepository(logger)
