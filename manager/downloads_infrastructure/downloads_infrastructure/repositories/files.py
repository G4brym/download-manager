import sqlite3
from typing import Optional

from sqlify import Sqlite3Sqlify

from downloads import FilesRepository, DownloadSettings
from downloads.domain.entities import File
from downloads.domain.value_objects import HashId


class SqlFilesRepository(FilesRepository):
    def __init__(self, database: Sqlite3Sqlify) -> None:
        self._database = database

    def get(self, hash: HashId) -> Optional[File]:
        obj = self._database.fetchone(
            table="downloads",
            where=("hash = :hash", dict(hash=hash)),
        )

        if not obj:
            return None

        return File.from_dict(obj)

    def save(self, file: File) -> None:
        try:
            self._database.insert(
                table="downloads",
                data=File.to_dict(file),
            )
        except sqlite3.IntegrityError:
            self._database.update(
                table="downloads",
                where=("hash = :hash", dict(hash=file.hash)),
                data=File.to_dict(file),
            )

    def retry_all(self) -> None:
        self._database.update(
            table="downloads",
            data=dict(failed=0, retries=0),
            where=[
                "failed <> 0",
                "completed = 0",
            ],
        )

    def get_next_to_download(self) -> Optional[File]:
        obj = self._database.fetchone(
            table="downloads",
            where=(
                [
                    "completed = 0",
                    "retries < :max_retries",
                ],
                dict(max_retries=DownloadSettings.MAX_RETRIES),
            ),
        )

        if not obj:
            return None

        return File.from_dict(obj)
