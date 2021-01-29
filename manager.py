import hashlib
import json
import logging
import os
import shutil
import sqlite3
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError

import atexit
import flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify, request, g
from pySmartDL import SmartDL


class NoRunningFilter(logging.Filter):
    def filter(self, record):
        return not record.msg.startswith("Execution of job")


logging.getLogger("apscheduler.scheduler").addFilter(NoRunningFilter())

app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
DOWNLOADS_PATH = os.environ.get("DOWNLOADS_PATH", "/downloads")
TMP_PATH = "/tmp/downloader/"
DATABASE = "config/db.sqlite3"
API_KEY = os.environ.get("API_KEY", "debug")
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 10))

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@scheduler.scheduled_job(trigger="interval", seconds=10, max_instances=1)
def download_scheduled_files():
    with app.app_context():
        file_to_download = query_db('SELECT * FROM downloads WHERE completed = 0 AND retries < ? LIMIT 1',
                                    [MAX_RETRIES], one=True)

    if not file_to_download:
        return

    tmp_folder = os.path.join(TMP_PATH, uuid.uuid4().hex)
    tmp_path = os.path.join(tmp_folder, file_to_download["name"])
    destination_path = os.path.join(DOWNLOADS_PATH, file_to_download["path"])

    try:
        app.logger.info("Starting download file {}".format(file_to_download["name"]))
        obj = SmartDL(file_to_download["url"], tmp_path, progress_bar=False,
                      request_args={"headers": json.loads(file_to_download["headers"])})
        obj.start()

        os.makedirs(destination_path, exist_ok=True)
        shutil.move(tmp_path, destination_path)

        with app.app_context():
            execute_db("UPDATE downloads SET completed = 1 WHERE hash = ?", [file_to_download["hash"]], commit=True)

        app.logger.info("Download Finished")
    except HTTPError:
        with app.app_context():
            execute_db("UPDATE downloads SET failed = 1, retries = retries + 1 WHERE hash = ?",
                       [file_to_download["hash"]], commit=True)
        shutil.rmtree(tmp_folder)
        app.logger.warning("Download Failed with error 1")
    except URLError:
        with app.app_context():
            execute_db("UPDATE downloads SET failed = 2, retries = retries + 1 WHERE hash = ?",
                       [file_to_download["hash"]], commit=True)
        shutil.rmtree(tmp_folder)
        app.logger.warning("Download Failed with error 2")
    except IOError:
        with app.app_context():
            execute_db("UPDATE downloads SET failed = 3, retries = retries + 1 WHERE hash = ?",
                       [file_to_download["hash"]], commit=True)
        shutil.rmtree(tmp_folder)
        app.logger.warning("Download Failed with error 3")


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
    db_folder = "/".join(DATABASE.split("/")[:-1])
    Path(os.path.join(LOCAL_PATH, db_folder)).mkdir(parents=True, exist_ok=True)

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
    if request.args.get('key') != API_KEY:
        return jsonify({}), 401

    data = request.get_json()
    result = []

    for link in data["links"]:
        # Default values for optional parameters
        link.setdefault("name", link["url"].split("/")[-1])
        link.setdefault("path", "")
        link.setdefault("headers", {})

        # Sanitize inputs
        if link["name"].startswith("/"):
            link["name"] = link["name"][1:]
        if link["path"].startswith("/"):
            link["path"] = link["path"][1:]
        if not link["path"].endswith("/"):
            link["path"] = "{}/".format(link["path"])

        headers = json.dumps(link["headers"])

        # File hash
        hash = hashlib.md5((link["path"] + link["name"]).encode("utf-8")).hexdigest()

        download_final_path = os.path.join(DOWNLOADS_PATH, link["path"], link["name"])
        download_exists = os.path.exists(download_final_path)

        try:
            # Schedule download
            execute_db('INSERT INTO downloads (hash, name, path, url, completed, headers) VALUES (?, ?, ?, ?, ?, ?)', [
                hash, link["name"], link["path"], link["url"], download_exists, headers
            ])
        except sqlite3.IntegrityError:
            # File already scheduled, returning current state
            _duplicated_file = query_db('SELECT * FROM downloads WHERE hash = ?', [hash], one=True)

            if _duplicated_file["url"] != link["url"] or _duplicated_file["headers"] != headers:
                execute_db("UPDATE downloads SET url = ?, headers = ?, failed = 0, retries = 0 WHERE hash = ?",
                           [link["url"], headers, hash])

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


@app.route('/api/v1/download/retry', methods=['post'])
def download_retry():
    if request.args.get('key') != API_KEY:
        return jsonify({}), 401

    execute_db("UPDATE downloads SET failed = 0, retries = 0 WHERE failed <> 0 AND completed = 0", commit=True)
    return jsonify({"status": "ok"})


@app.route('/api/v1/download/<hash>', methods=['post'])
def single_download_retry(hash):
    if request.args.get('key') != API_KEY:
        return jsonify({}), 401

    download = query_db('SELECT * FROM downloads WHERE hash = ?', [hash], one=True)
    if not download:
        return jsonify({}), 404

    execute_db("UPDATE downloads SET failed = 0, retries = 0 WHERE hash = ?", [hash], commit=True)
    return jsonify({"status": "ok"})


@app.route('/api/v1/download/status/', methods=['POST'])
def download_bulk_status():
    if request.args.get('key') != API_KEY:
        return jsonify({}), 401

    data = request.get_json()
    files = data.get("files", [])
    downloads = query_db(f"SELECT * FROM downloads WHERE hash in ({','.join(['?']*len(files))})", files)

    return jsonify(
        {
            download["hash"]: {
                "hash": download["hash"],
                "name": download["name"],
                "path": download["path"],
                "url": download["url"],
                "failed": download["failed"],
                "completed": bool(download["completed"])
            } for download in downloads
        }
    )


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


# Create table on boot
init_db()

if __name__ == '__main__':
    app.run()
