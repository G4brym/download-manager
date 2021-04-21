from typing import List, Optional

from downloads import GetTotalFiles, GetFileStatus, GetBulkFileStatus, HashId, FileDto
from downloads.domain.entities import File
from downloads_infrastructure.queries.base import SqlQuery


class SqlGetTotalFiles(GetTotalFiles, SqlQuery):
    def query(self) -> int:
        return self._database.query(
            "select count(*) as count from downloads", one=True
        )["count"]


class SqlGetFileStatus(GetFileStatus, SqlQuery):
    def query(self, hash: HashId) -> Optional[FileDto]:
        obj = self._database.query(
            "SELECT * FROM downloads WHERE hash = ?", [hash], one=True
        )
        if not obj:
            return None

        return FileDto.from_file(File.from_dict(obj))


class SqlGetBulkFileStatus(GetBulkFileStatus, SqlQuery):
    def query(self, hash_list: List[HashId]) -> List[FileDto]:
        obj_list = self._database.query(
            "SELECT * FROM downloads WHERE hash in ?", [hash_list]
        )

        return [FileDto.from_file(File.from_dict(obj)) for obj in obj_list]
