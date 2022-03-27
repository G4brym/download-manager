from sqlify import Sqlite3Sqlify

from downloads import GetDownloadStatus, DownloadSettings
from downloads.domain.entities import DownloadStatus


class SqlGetDownloadStatus(GetDownloadStatus):
    def __init__(self, database: Sqlite3Sqlify) -> None:
        self._database = database

    def query(self) -> DownloadStatus:
        total = self._database.fetchone(
            table="downloads",
            fields=[
                "count(*) as total",
            ],
        )["total"]

        completed = self._database.fetchone(
            table="downloads",
            fields=[
                "count(*) as completed",
            ],
            where="completed = 1",
        )["completed"]

        not_completed = self._database.fetchone(
            table="downloads",
            fields=[
                "count(*) as not_completed",
            ],
            where=(
                [
                    "completed = 0",
                    "retries < :max_retries",
                ],
                dict(max_retries=DownloadSettings.MAX_RETRIES),
            ),
        )["not_completed"]

        not_completed_and_failed = self._database.fetchone(
            table="downloads",
            fields=[
                "count(*) as not_completed_and_failed",
            ],
            where=(
                [
                    "completed = 0",
                    "retries >= :max_retries",
                ],
                dict(max_retries=DownloadSettings.MAX_RETRIES),
            ),
        )["not_completed_and_failed"]

        return DownloadStatus(
            total=total,
            completed=completed,
            not_completed=not_completed,
            not_completed_and_failed=not_completed_and_failed,
        )
