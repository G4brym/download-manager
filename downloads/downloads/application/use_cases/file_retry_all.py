from downloads.application.repositories import FilesRepository


class FileRetryAll:
    def __init__(self, files_repo: FilesRepository) -> None:
        self.files_repo = files_repo

    def execute(self) -> None:
        self.files_repo.retry_all()
