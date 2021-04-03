import logging

from fastapi.logger import logger as app_logger

app_logger.handlers = logging.getLogger("gunicorn.error").handlers
app_logger.setLevel(logging.INFO)


class NoRunningFilter(logging.Filter):
    def filter(self, record):
        return not record.msg.startswith("Execution of job")


scheduler_logger = logging.getLogger("apscheduler.scheduler")
scheduler_logger.addFilter(NoRunningFilter())

__all__ = ["app_logger"]
