import os
import sqlite3
from pathlib import Path

from cuttlepool import CuttlePool

from common.database_service import DatabaseService
from common.settings import DATABASE_PATH, BASE_PATH


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLitePool(CuttlePool):
    def normalize_resource(self, resource):
        resource.row_factory = dict_factory

    def ping(self, resource):
        try:
            rv = resource.execute("SELECT 1").fetchall()
            return (1,) in rv
        except sqlite3.Error:
            return False


pool = SQLitePool(
    factory=sqlite3.connect, database=DATABASE_PATH, capacity=2, timeout=60
)


class DatabaseHandler(DatabaseService):
    def initial_migration(self):
        database_folder = "/".join(DATABASE_PATH.split("/")[:-1])
        Path(database_folder).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(BASE_PATH, "schema.sql"), mode="r") as f:
            with pool.get_resource() as con:
                cur = con.cursor().executescript(f.read())
                cur.close()
                con.commit()

    def query(self, query, args=(), one=False):
        with pool.get_resource() as con:
            cur = con.execute(query, args)
            rv = cur.fetchall()
            cur.close()
        return (rv[0] if rv else None) if one else rv

    def execute(self, query, args=()):
        with pool.get_resource() as con:
            cur = con.execute(query, args)
            con.commit()
            cur.close()
