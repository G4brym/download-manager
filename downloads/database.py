import os
import sqlite3
from pathlib import Path

from flask import g

from downloads.core import DATABASE_PATH, BASE_PATH


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DatabaseHandler:
    _app = None

    def init_app(self, app):
        self._app = app

        with app.app_context():
            self.initial_migration()

        @app.teardown_appcontext
        def close_connection(exception):
            self.close()

    @property
    def db_conn(self):
        db_conn = getattr(g, '_database', None)
        if db_conn is None:
            db_conn = g._database = sqlite3.connect(DATABASE_PATH)

        db_conn.row_factory = dict_factory
        return db_conn

    def initial_migration(self):
        database_folder = "/".join(DATABASE_PATH.split("/")[:-1])
        Path(database_folder).mkdir(parents=True, exist_ok=True)

        with self._app.app_context():
            with self._app.open_resource(os.path.join(BASE_PATH, "schema.sql"), mode='r') as f:
                self.db_conn.cursor().executescript(f.read())

            self.db_conn.commit()

    def query(self, query, args=(), one=False):
        cur = self.db_conn.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def execute(self, query, args=()):
        cur = self.db_conn.execute(query, args)
        cur.close()
        self.db_conn.commit()

    def close(self):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()


db = DatabaseHandler()
