import sqlite3
import uuid
from datetime import datetime, date
from decimal import Decimal
from logging import Logger
from sqlite3 import Connection
from typing import get_type_hints, Optional, Any

import injector
from sqlify import Session, Sqlite3Sqlify

from common.settings import DATABASE_PATH
from downloads import Downloads
from downloads_infrastructure import DownloadsInfrastructure
from common.logger import provide_logger

__all__ = [
    "provider",
]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Common(injector.Module):
    @injector.provider
    @injector.singleton
    def logger(self) -> Logger:
        return provide_logger()

    @injector.provider
    def database_connection(self) -> Connection:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = dict_factory
        return conn

    @injector.provider
    def database(self, database_connection: Connection) -> Sqlite3Sqlify:
        return Session(database_connection, autocommit=True).session


class ProvideManager(object):
    def __init__(self):
        self.injector = injector.Injector(
            [
                Common(),
                Downloads(),
                DownloadsInfrastructure(),
            ],
            auto_bind=True,
        )
        self.blacklist = [str, int, float, Decimal, datetime, date, bool, uuid.UUID]

    def get_instance(self, arg_type: Any) -> Optional[Any]:
        if arg_type in self.blacklist:
            return None

        try:
            _provided = self.injector.get(arg_type)
            if _provided is not None and bool(_provided) is not False:
                return _provided
        except (injector.CallError, injector.UnknownProvider, TypeError):
            pass

        return None

    def inject(self, func):
        def wrapper(*args, **kwargs):
            for arg_name, arg_type in get_type_hints(func).items():
                _instance = self.get_instance(arg_type)
                if _instance:
                    kwargs[arg_name] = self.get_instance(arg_type)

            return func(*args, **kwargs)

        return wrapper


provider = ProvideManager()
