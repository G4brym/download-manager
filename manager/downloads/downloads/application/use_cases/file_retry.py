from downloads.application.repositories import FilesRepository
from downloads.domain.value_objects import HashId, FailTypes


class FileRetry:
    def __init__(self, files_repo: FilesRepository) -> None:
        self.files_repo = files_repo

    def execute(self, hash: HashId) -> bool:
        file = self.files_repo.get(hash)

        if not file:
            return False

        self.files_repo.save(
            file.copy_with(
                failed=FailTypes.NoError,
                retries=0,
            )
        )

        return True
