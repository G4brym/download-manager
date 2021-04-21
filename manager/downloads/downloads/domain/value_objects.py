from enum import Enum

HashId = str


class FailTypes(Enum):
    NoError = 0
    ServerError = 1
    ReachingError = 2
    LocalIOError = 3
