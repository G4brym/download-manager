import abc
from typing import Dict, Optional

from downloads.domain.value_objects import FailTypes


class DownloadRepository(abc.ABC):
    @abc.abstractmethod
    def download_file(
        self, url: str, name: str, path: str, headers: Optional[Dict[str, str]]
    ) -> FailTypes:
        pass
