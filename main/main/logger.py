import logging


def provide_logger():
    from fastapi.logger import logger as app_logger

    app_logger.handlers = logging.getLogger("gunicorn.error").handlers
    app_logger.setLevel(logging.INFO)

    return app_logger
