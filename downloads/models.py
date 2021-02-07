import hashlib
import json
import os
import sqlite3
from typing import Dict, List

from downloads.core import DOWNLOADS_PATH, MAX_RETRIES
from downloads.database import db


class Download:
    hash: str  # Primary Key
    name: str
    path: str
    url: str
    headers: Dict

    completed: bool
    retries: int

    # 1 => Server error
    # 2 => Problem reaching the server
    # 3 => Local IO problems (maybe no disk space available)
    failed: int

    def __init__(self, url: str, path: str, name: str = None, hash: str = None, headers: Dict = None,
                 completed: bool = False,
                 retries: int = 0, failed: int = 0):
        self.url = url
        if path.startswith("/"):
            path = path[1:]
        if not path.endswith("/"):
            path = "{}/".format(path)
        self.path = path

        if not name:
            name = url.split("/")[-1]
        if name.startswith("/"):
            name = name[1:]
        self.name = name

        if not hash:
            hash = hashlib.md5((path + name).encode("utf-8")).hexdigest()
        self.hash = hash

        if not completed:
            completed = os.path.exists(os.path.join(DOWNLOADS_PATH, path, name))
        self.completed = completed

        self.retries = retries
        self.failed = failed

        if not headers:
            headers = {}
        self.headers = headers

    @property
    def destination_path(self):
        return os.path.join(DOWNLOADS_PATH, self.path)

    @classmethod
    def count(cls):
        return db.query('select count(*) from downloads', one=True)[0]

    @classmethod
    def retry_all(cls):
        db.execute('UPDATE downloads SET failed = 0, retries = 0 WHERE failed <> 0 AND completed = 0')
        return True

    @classmethod
    def get_by_hash(cls, hash: str):
        return Download.loads(db.query('SELECT * FROM downloads WHERE hash = ?', [hash], one=True))

    @classmethod
    def get_next_to_download(cls):
        return Download.loads(
            db.query('SELECT * FROM downloads WHERE completed = 0 AND retries < ? LIMIT 1', [MAX_RETRIES], one=True))

    @classmethod
    def list_by_hash(cls, hash_list: List[str]):
        return [
            Download.loads(file)
            for file in
            db.query(f"SELECT * FROM downloads WHERE hash in ({','.join(['?'] * len(hash_list))})", hash_list)
        ]

    @classmethod
    def loads(cls, config: Dict):
        return cls(
            hash=config["hash"],
            name=config["name"],
            path=config["path"],
            url=config["url"],
            headers=json.loads(config["headers"]),
            completed=config["completed"],
        )

    @classmethod
    def dumps(cls, download):
        return {
            "hash": download.hash,
            "name": download.name,
            "path": download.path,
            "url": download.url,
            "failed": download.failed,
            "retries": download.retries,
            "completed": download.completed
        }

    def save(self):
        try:
            db.execute("INSERT INTO downloads (hash, name, path, url, completed, headers) VALUES (?, ?, ?, ?, ?, ?)", [
                self.hash, self.name, self.path, self.url, self.completed, json.dumps(self.headers)
            ])
        except sqlite3.IntegrityError:
            db.execute("UPDATE downloads SET name = ?, path = ?, url = ?, completed = ?, headers = ? WHERE hash = ?", [
                self.name, self.path, self.url, self.completed, json.dumps(self.headers), self.hash
            ])
        return True
