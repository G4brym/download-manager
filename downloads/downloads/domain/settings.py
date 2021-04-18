import os

DOWNLOADS_PATH = os.environ.get("DOWNLOADS_PATH", "/downloads")
TMP_PATH = "/tmp/downloader/"

API_KEY = os.environ.get("API_KEY", "debug")
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 10))
