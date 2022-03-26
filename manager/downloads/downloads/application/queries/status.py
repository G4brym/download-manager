import abc

from ...domain.entities import DownloadStatus


class GetDownloadStatus(abc.ABC):
    @abc.abstractmethod
    def query(self) -> DownloadStatus:
        pass
