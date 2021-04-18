import json
import sqlite3
from typing import Optional

from downloads import FilesRepository
from downloads.domain.entities import File
from downloads.domain.settings import MAX_RETRIES
from downloads.domain.value_objects import HashId
from main.database_service import DatabaseService


class SqlFilesRepository(FilesRepository):
    def __init__(self, database: DatabaseService) -> None:
        self._database = database

    def get(self, hash: HashId) -> Optional[File]:
        obj = self._database.query(
            "SELECT * FROM downloads WHERE hash = ?", [hash], one=True
        )
        if not obj:
            return None

        return File.from_dict(obj)

    def save(self, file: File) -> None:
        file_dump = File.to_dict(file)
        try:
            self._database.execute(
                "INSERT INTO downloads (hash, name, path, url, failed, completed, retries, headers, creation_date, "
                "completion_date) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    file_dump["hash"],
                    file_dump["name"],
                    file_dump["path"],
                    file_dump["url"],
                    file_dump["failed"],
                    file_dump["completed"],
                    file_dump["retries"],
                    json.dumps(file_dump["headers"]),
                    file_dump["creation_date"],
                    file_dump["completion_date"],
                ],
            )
        except sqlite3.IntegrityError:
            self._database.execute(
                "UPDATE downloads SET name = ?, path = ?, url = ?, failed = ?, completed = ?, retries = ?, "
                "headers = ?, creation_date = ?, completion_date = ?  WHERE hash = ?",
                [
                    file_dump["name"],
                    file_dump["path"],
                    file_dump["url"],
                    file_dump["failed"],
                    file_dump["completed"],
                    file_dump["retries"],
                    json.dumps(file_dump["headers"]),
                    file_dump["creation_date"],
                    file_dump["completion_date"],
                    file_dump["hash"],
                ],
            )

    def retry_all(self) -> None:
        self._database.execute(
            "UPDATE downloads SET failed = 0, retries = 0 WHERE failed <> 0 AND completed = 0"
        )

    def get_next_to_download(self) -> Optional[File]:
        obj = self._database.query(
            "SELECT * FROM downloads WHERE completed = 0 AND retries < ?",
            [MAX_RETRIES],
            one=True,
        )
        if not obj:
            return None

        return File.from_dict(obj)
