import uuid
from datetime import datetime, date
from decimal import Decimal
from logging import Logger
from typing import get_type_hints, Optional, Any

import injector

from downloads import Downloads
from downloads_infrastructure import DownloadsInfrastructure
from common.database import DatabaseHandler
from common.database_service import DatabaseService
from common.logger import provide_logger

__all__ = [
    "provider",
    "DatabaseService",
]


class Common(injector.Module):
    @injector.provider
    @injector.singleton
    def logger(self) -> Logger:
        return provide_logger()

    @injector.provider
    @injector.singleton
    def database(self) -> DatabaseService:
        return DatabaseHandler()


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
