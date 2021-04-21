from logging import Logger

import injector

__all__ = [
    # module
    "DownloadsInfrastructure",
]

from downloads import (
    GetTotalFiles,
    GetFileStatus,
    GetBulkFileStatus,
    FilesRepository,
    DownloadRepository,
)
from downloads_infrastructure.queries import (
    SqlGetTotalFiles,
    SqlGetFileStatus,
    SqlGetBulkFileStatus,
)
from downloads_infrastructure.repositories import (
    SqlFilesRepository,
    SmartDLDownloadRepository,
)
from common.database import DatabaseService


class DownloadsInfrastructure(injector.Module):
    @injector.provider
    def get_total_files(self, database: DatabaseService) -> GetTotalFiles:
        return SqlGetTotalFiles(database)

    @injector.provider
    def get_file_status(self, database: DatabaseService) -> GetFileStatus:
        return SqlGetFileStatus(database)

    @injector.provider
    def get_bulk_file_status(self, database: DatabaseService) -> GetBulkFileStatus:
        return SqlGetBulkFileStatus(database)

    @injector.provider
    def files_repo(self, database: DatabaseService) -> FilesRepository:
        return SqlFilesRepository(database)

    @injector.provider
    def download_repo(self, logger: Logger) -> DownloadRepository:
        return SmartDLDownloadRepository(logger)
