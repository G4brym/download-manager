from typing import List, Optional

from sqlify import Sqlite3Sqlify

from downloads import GetFileStatus, GetBulkFileStatus, HashId, FileDto
from downloads.domain.entities import File


class SqlGetFileStatus(GetFileStatus):
    def __init__(self, database: Sqlite3Sqlify) -> None:
        self._database = database

    def query(self, hash: HashId) -> Optional[FileDto]:
        obj = self._database.fetchone(
            table="downloads",
            where=("hash = :hash", dict(hash=hash)),
        )

        if not obj:
            return None

        return FileDto.from_file(File.from_dict(obj))


class SqlGetBulkFileStatus(GetBulkFileStatus):
    def __init__(self, database: Sqlite3Sqlify) -> None:
        self._database = database

    def query(self, hash_list: List[HashId]) -> List[FileDto]:
        obj_list = self._database.fetchall(
            table="downloads",
            where=("id in :hash_list", dict(hash_list=hash_list)),
        )

        return [FileDto.from_file(File.from_dict(obj)) for obj in obj_list]
