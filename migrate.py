import os

from sqlify import Sqlite3Sqlify

from common import provider
from common.settings import BASE_PATH, DATABASE_PATH
from pathlib import Path


@provider.inject
def migrate(database: Sqlite3Sqlify):
    database_folder = "/".join(DATABASE_PATH.split("/")[:-1])
    Path(database_folder).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(BASE_PATH, "schema.sql"), mode="r") as f:
        database.execute(f.read())

    print("Migration applied!")


migrate()
