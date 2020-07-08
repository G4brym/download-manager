import hashlib
import sqlite3

import flask
from flask import jsonify, request, g

DATABASE = 'database.db'
app = flask.Flask(__name__)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(query, args=()):
    cur = get_db().execute(query, args)
    cur.close()


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
        link.setdefault("name", link["url"].split("/")[-1])
        link.setdefault("path", "/")

        hash = hashlib.md5((link["path"] + link["name"]).encode("utf-8")).hexdigest()

        try:
            insert_db('INSERT INTO downloads (hash, name, path) VALUES (?, ?, ?)', [
                hash, link["name"], link["path"]
            ])
        except sqlite3.IntegrityError:
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

    get_db().commit()

    return jsonify({
        "downloads": result
    })


init_db()
app.run()
