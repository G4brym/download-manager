from datetime import datetime
from logging import Logger

from downloads.application.repositories import FilesRepository, DownloadRepository
from downloads.domain.value_objects import FailTypes


class TaskDownloadFile:
    def __init__(
        self,
        files_repo: FilesRepository,
        downloader_repo: DownloadRepository,
        logger: Logger,
    ) -> None:
        self.files_repo = files_repo
        self.downloader_repo = downloader_repo
        self.logger = logger

    def execute(self) -> None:
        file = self.files_repo.get_next_to_download()

        if not file:
            self.logger.info("No downloads in queue")
            return

        self.logger.info("Starting download file {}".format(file.name))
        _result = self.downloader_repo.download_file(
            url=file.url,
            name=file.name,
            path=file.path,
            headers=file.headers,
        )

        if _result == FailTypes.NoError:
            updated_file = file.copy_with(
                completed=True,
                failed=FailTypes.NoError,
                creation_date=datetime.now(),
            )

            self.logger.info("Download Finished")
        else:
            updated_file = file.copy_with(
                completed=False,
                retries=file.retries + 1,
                failed=_result,
            )

            self.logger.warning(
                "Download Failed with error {}: {}".format(_result.value, str(_result))
            )

        self.files_repo.save(updated_file)
