import sentry_sdk

from common import provide_logger
from common.settings import SENTRY_DSN

logger = provide_logger()

if SENTRY_DSN:
    sentry_sdk.init(
        SENTRY_DSN,
    )
    logger.info(f"Sentry Started with DSN: {SENTRY_DSN}")
