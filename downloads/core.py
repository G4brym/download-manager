import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DATABASE_PATH = os.path.join(BASE_PATH, os.environ.get("DATBASE_PATH", "config/db.sqlite3"))
DOWNLOADS_PATH = os.environ.get("DOWNLOADS_PATH", "/downloads")
TMP_PATH = "/tmp/downloader/"

API_KEY = os.environ.get("API_KEY", "debug")
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 10))
