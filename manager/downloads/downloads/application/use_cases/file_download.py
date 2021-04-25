from datetime import datetime
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
            creation_date=datetime.now(),
        )

        # Check if this file was already downloaded
        _previous_file = self.files_repo.get(file.hash)
        if _previous_file is not None:
            # File already exists, we only need to update url, headers and retry the file again, if no already completed
            file = _previous_file.copy_with(
                url=url,
                headers=headers,
                retries=0,
            )

        self.files_repo.save(file)
        return file
