import atexit
import logging
import os
import shutil
import uuid
from urllib.error import HTTPError, URLError

from apscheduler.schedulers.background import BackgroundScheduler
from pySmartDL import SmartDL

from downloads.core import TMP_PATH
from downloads.models import Download


class NoRunningFilter(logging.Filter):
    def filter(self, record):
        return not record.msg.startswith("Execution of job")


logger = logging.getLogger("apscheduler.scheduler")
logger.addFilter(NoRunningFilter())

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@scheduler.scheduled_job(trigger="interval", seconds=10, max_instances=1)
def download_scheduled_files():
    download = Download.get_next_to_download()

    if not download:
        return

    tmp_folder = os.path.join(TMP_PATH, uuid.uuid4().hex)
    tmp_path = os.path.join(tmp_folder, download.name)

    try:
        logger.info("Starting download file {}".format(download.name))
        obj = SmartDL(download.url, tmp_path, progress_bar=False,
                      request_args={"headers": download.headers})
        obj.start()

        os.makedirs(download.destination_path, exist_ok=True)
        shutil.move(tmp_path, download.destination_path)

        download.completed = True
        download.save()

        logger.info("Download Finished")
    except HTTPError:
        download.failed = 1
        download.retries = download.retries + 1
        download.save()

        logger.warning("Download Failed with error 1")
    except URLError:
        download.failed = 2
        download.retries = download.retries + 1
        download.save()

        logger.warning("Download Failed with error 2")
    except IOError:
        download.failed = 3
        download.retries = download.retries + 1
        download.save()

        logger.warning("Download Failed with error 3")
    finally:
        shutil.rmtree(tmp_folder)
