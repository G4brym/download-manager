import os
import shutil
import uuid
from urllib.error import HTTPError, URLError

from apscheduler.schedulers.background import BackgroundScheduler
from pySmartDL import SmartDL

from downloads.core import TMP_PATH
from downloads.logging import app_logger
from downloads.models import Download


def download_scheduled_files():
    download = Download.get_next_to_download()

    if not download:
        app_logger.info("No downloads in queue")
        return

    tmp_folder = os.path.join(TMP_PATH, uuid.uuid4().hex)
    tmp_path = os.path.join(tmp_folder, download.name)

    try:
        app_logger.info("Starting download file {}".format(download.name))
        headers = download.headers
        headers.setdefault("User-Agent", "DownloadManager 1.0")

        obj = SmartDL(download.url, tmp_path, progress_bar=False,
                      request_args={"headers": headers})
        obj.start()

        os.makedirs(download.destination_path, exist_ok=True)
        shutil.move(tmp_path, download.destination_path)

        download.completed = True
        download.save()

        app_logger.info("Download Finished")
    except HTTPError as e:
        download.failed = 1
        download.retries = download.retries + 1
        download.save()

        app_logger.warning("Download Failed with error 1 (HTTPError): {}".format(str(e)))
    except URLError:
        download.failed = 2
        download.retries = download.retries + 1
        download.save()

        app_logger.warning("Download Failed with error 2 (URLError): {}".format(str(e)))
    except IOError:
        download.failed = 3
        download.retries = download.retries + 1
        download.save()

        app_logger.warning("Download Failed with error 3 (IOError): {}".format(str(e)))
    finally:
        shutil.rmtree(tmp_folder, ignore_errors=True)


scheduler = BackgroundScheduler()
scheduler.add_job(download_scheduled_files, 'interval', seconds=10, max_instances=1)
