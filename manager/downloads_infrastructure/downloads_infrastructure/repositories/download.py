import os
import shutil
import uuid
from logging import Logger
from os.path import exists
from typing import Dict, Optional
from urllib.error import HTTPError, URLError

from pySmartDL import SmartDL

from downloads import DownloadRepository, FailTypes, DownloadSettings


class SmartDLDownloadRepository(DownloadRepository):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def download_file(
        self, url: str, name: str, path: str, headers: Optional[Dict[str, str]]
    ) -> FailTypes:
        tmp_folder = os.path.join(DownloadSettings.TMP_PATH, uuid.uuid4().hex)
        tmp_path = os.path.join(tmp_folder, name)

        if exists(path):
            self.logger.warning(f"File {name} already exists in path {path}")

        try:
            _tmp_headers = headers
            _tmp_headers.setdefault("User-Agent", "DownloadManager 1.0")

            obj = SmartDL(
                url,
                tmp_path,
                progress_bar=False,
                request_args={"headers": _tmp_headers},
            )
            obj.start()

            os.makedirs(path, exist_ok=True)
            shutil.move(tmp_path, path)

            return FailTypes.NoError
        except HTTPError as e:
            self.logger.warning(
                "Download Failed with error 1 (HTTPError): {}".format(str(e))
            )
            return FailTypes.ServerError

        except URLError as e:
            self.logger.warning(
                "Download Failed with error 2 (URLError): {}".format(str(e))
            )
            return FailTypes.ReachingError

        except IOError as e:
            self.logger.warning(
                "Download Failed with error 3 (IOError): {}".format(str(e))
            )
            return FailTypes.LocalIOError

        finally:
            shutil.rmtree(tmp_folder, ignore_errors=True)
