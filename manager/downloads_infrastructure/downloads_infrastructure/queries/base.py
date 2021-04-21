from common.database_service import DatabaseService


class SqlQuery:
    def __init__(self, database: DatabaseService) -> None:
        self._database = database
