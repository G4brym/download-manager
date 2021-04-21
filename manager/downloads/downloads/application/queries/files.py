import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict

from downloads.domain.entities import File
from downloads.domain.value_objects import HashId


@dataclass
class FileDto:
    hash: HashId
    name: str
    path: str
    url: str
    failed: int
    retries: int
    completed: bool
    creation_date: datetime
    completion_date: Optional[datetime] = None
    headers: Optional[Dict[str, str]] = None

    @classmethod
    def from_file(cls, record: File):
        record = File.to_dict(record)
        return cls(
            hash=record["hash"],
            name=record["name"],
            path=record["path"],
            url=record["url"],
            failed=record["failed"],
            retries=record["retries"],
            creation_date=record["creation_date"],
            completed=record["completed"],
            completion_date=record["completion_date"],
            headers=record["headers"],
        )


class GetTotalFiles(abc.ABC):
    @abc.abstractmethod
    def query(self) -> int:
        pass


class GetFileStatus(abc.ABC):
    @abc.abstractmethod
    def query(self, hash: HashId) -> Optional[FileDto]:
        pass


class GetBulkFileStatus(abc.ABC):
    @abc.abstractmethod
    def query(self, hash_list: List[HashId]) -> List[FileDto]:
        pass
