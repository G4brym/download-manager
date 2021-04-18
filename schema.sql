CREATE TABLE IF NOT EXISTS downloads
(
    hash TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    url TEXT NOT NULL,
    failed INTEGER DEFAULT 0,
    completed INTEGER DEFAULT 0,
    retries INTEGER DEFAULT 0,
    headers TEXT DEFAULT '{}'
);

alter table downloads
    add creation_date datetime default now not null;

alter table downloads
    add completion_date datetime;
