import logging

from apscheduler.schedulers.background import BackgroundScheduler

from downloads import TaskDownloadFile
from main import provider


class NoRunningFilter(logging.Filter):
    def filter(self, record):
        return not record.msg.startswith("Execution of job")


scheduler_logger = logging.getLogger("apscheduler.scheduler")
scheduler_logger.addFilter(NoRunningFilter())


@provider.inject()
def execute_task_download_file(task_download_file_uc: TaskDownloadFile):
    task_download_file_uc.execute()


scheduler = BackgroundScheduler()
scheduler.add_job(execute_task_download_file, "interval", seconds=10, max_instances=1)
