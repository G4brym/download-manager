import abc
from typing import Optional

from downloads.domain.entities import File
from downloads.domain.value_objects import HashId


class FilesRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, hash: HashId) -> Optional[File]:
        pass

    @abc.abstractmethod
    def save(self, file: File) -> None:
        pass

    @abc.abstractmethod
    def retry_all(self) -> None:
        pass

    @abc.abstractmethod
    def get_next_to_download(self) -> Optional[File]:
        pass
