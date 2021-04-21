import os

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)

DATABASE_PATH = os.environ.get("DATABASE_PATH", "/config/db.sqlite3")
if not os.path.isabs(DATABASE_PATH):
    DATABASE_PATH = os.path.join(BASE_PATH, DATABASE_PATH)

LOGGING_CONFIG = os.path.join(BASE_PATH, "logging.yml")
