import sqlite3
from typing import Dict, Optional

from downloads.application.repositories import FilesRepository
from downloads.domain.entities import File


class FileDownload:
    def __init__(self, files_repo: FilesRepository) -> None:
        self.files_repo = files_repo

    def execute(
        self, name: str, path: str, url: str, headers: Dict[str, str]
    ) -> Optional[File]:
        file = File(
            name=name,
            path=path,
            url=url,
            headers=headers,
        )

        try:
            self.files_repo.save(file)
        except sqlite3.IntegrityError:
            return None

        return file
