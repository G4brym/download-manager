import sentry_sdk

from common import provide_logger
from common.settings import CommonSettings

logger = provide_logger()

if CommonSettings.SENTRY_DSN:
    sentry_sdk.init(
        CommonSettings.SENTRY_DSN,
    )
    logger.info(f"Sentry Started with DSN: {CommonSettings.SENTRY_DSN}")
