import atexit
import hashlib
import os
import sqlite3
from urllib.error import HTTPError, URLError

import flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify, request, g
from pySmartDL import SmartDL

DATABASE = 'database.db'
app = flask.Flask(__name__)
local_path = os.path.dirname(os.path.realpath(__file__))

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@scheduler.scheduled_job(trigger="interval", seconds=10, max_instances=1)
def download_scheduled_files():
    with app.app_context():
        file_to_download = query_db('SELECT * FROM downloads WHERE completed = 0 AND failed = 0 LIMIT 1', one=True)

    if not file_to_download:
        return

    destination_path = os.path.join(local_path, file_to_download["path"], file_to_download["name"])

    try:
        obj = SmartDL(file_to_download["url"], destination_path, progress_bar=True)
        obj.start()
    except HTTPError:
        with app.app_context():
            execute_db("UPDATE downloads SET failed = 1 WHERE hash = ?", [file_to_download["hash"]], commit=True)
    except URLError:
        with app.app_context():
            execute_db("UPDATE downloads SET failed = 2 WHERE hash = ?", [file_to_download["hash"]], commit=True)
    except IOError:
        with app.app_context():
            execute_db("UPDATE downloads SET failed = 3 WHERE hash = ?", [file_to_download["hash"]], commit=True)
    finally:
        with app.app_context():
            execute_db("UPDATE downloads SET completed = 1 WHERE hash = ?", [file_to_download["hash"]], commit=True)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=(), commit=False):
    cur = get_db().execute(query, args)
    cur.close()
    if commit:
        get_db().commit()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def api_index():
    count = query_db('select count(*) from downloads', one=True)
    return jsonify({"status": "ok", "downloads": count[0]})


@app.route('/api/v1/download', methods=['POST'])
def api_download():
    data = request.get_json()
    result = []

    for link in data["links"]:
        # Default values for optional parameters
        link.setdefault("name", link["url"].split("/")[-1])
        link.setdefault("path", "")

        # Sanitize inputs
        if link["name"].startswith("/"):
            link["name"] = link["name"][1:]
        if link["path"].startswith("/"):
            link["path"] = link["path"][1:]
        if not link["path"].endswith("/"):
            link["path"] = "{}/".format(link["path"])

        # File hash
        hash = hashlib.md5((link["path"] + link["name"]).encode("utf-8")).hexdigest()

        try:
            # Schedule download
            execute_db('INSERT INTO downloads (hash, name, path, url) VALUES (?, ?, ?, ?)', [
                hash, link["name"], link["path"], link["url"]
            ])
        except sqlite3.IntegrityError:
            # File already scheduled, returning current state
            _duplicated_file = query_db('SELECT * FROM downloads WHERE hash = ?', [hash], one=True)

            result.append({
                "id": hash,
                "name": link["name"],
                "completed": bool(_duplicated_file["completed"])
            })

            continue

        result.append({
            "id": hash,
            "name": link["name"],
            "completed": False
        })

    # Save to db
    get_db().commit()

    # Return list of scheduled downloads
    return jsonify({
        "downloads": result
    })


@app.route('/api/v1/download/<hash>', methods=['GET'])
def download_status(hash):
    download = query_db('SELECT * FROM downloads WHERE hash = ?', [hash], one=True)
    if not download:
        return jsonify({}), 404

    return jsonify({
        "hash": download["hash"],
        "name": download["name"],
        "path": download["path"],
        "url": download["url"],
        "failed": download["failed"],
        "completed": bool(download["completed"])
    })


if __name__ == '__main__':
    # Create table on boot
    init_db()
    app.run()
