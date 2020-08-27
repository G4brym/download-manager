import logging
import os
import sqlite3
from pathlib import Path

import flask
from flask import g

app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
DATABASE = "config/db.sqlite3"


def migrate_db():
    db_folder = "/".join(DATABASE.split("/")[:-1])
    Path(os.path.join(LOCAL_PATH, db_folder)).mkdir(parents=True, exist_ok=True)

    with app.app_context():
        db = get_db()
        with app.open_resource('update.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    return db


# Migrate
migrate_db()
