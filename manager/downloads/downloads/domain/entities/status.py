from dataclasses import dataclass


@dataclass
class DownloadStatus:
    total: int
    completed: int
    not_completed: int
    not_completed_and_failed: int
