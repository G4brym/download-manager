import logging

from apscheduler.schedulers.background import BackgroundScheduler

from common import provider
from downloads import TaskDownloadFile


class NoRunningFilter(logging.Filter):
    def filter(self, record):
        return not record.msg.startswith("Execution of job")


scheduler_logger = logging.getLogger("apscheduler.scheduler")
scheduler_logger.addFilter(NoRunningFilter())


def run_schedule():
    @provider.inject
    def execute_task_download_file(task_download_file_uc: TaskDownloadFile):
        task_download_file_uc.execute()

    execute_task_download_file()


scheduler = BackgroundScheduler()
scheduler.add_job(run_schedule, "interval", seconds=10, max_instances=1)
