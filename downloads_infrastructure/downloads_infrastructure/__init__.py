from logging import Logger

import injector

__all__ = [
    # module
    "DownloadsInfrastructure",
]

from downloads_infrastructure.queries import (
    SqlGetTotalFiles,
    SqlGetFileStatus,
    SqlGetBulkFileStatus,
)
from downloads_infrastructure.repositories import (
    SqlFilesRepository,
    SmartDLDownloadRepository,
)
from main.database import DatabaseService


class DownloadsInfrastructure(injector.Module):
    @injector.provider
    def get_total_files(self, database: DatabaseService) -> SqlGetTotalFiles:
        return SqlGetTotalFiles(database)

    @injector.provider
    def get_file_status(self, database: DatabaseService) -> SqlGetFileStatus:
        return SqlGetFileStatus(database)

    @injector.provider
    def get_bulk_file_status(self, database: DatabaseService) -> SqlGetBulkFileStatus:
        return SqlGetBulkFileStatus(database)

    @injector.provider
    def files_repo(self, database: DatabaseService) -> SqlFilesRepository:
        return SqlFilesRepository(database)

    @injector.provider
    def download_repo(self, logger: Logger) -> SmartDLDownloadRepository:
        return SmartDLDownloadRepository(logger)
