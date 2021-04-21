import logging


def provide_logger():
    from fastapi.logger import logger as app_logger

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app_logger.handlers.extend(gunicorn_error_logger.handlers)

    return gunicorn_error_logger
