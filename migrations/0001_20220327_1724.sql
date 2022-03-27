-- Migration number: 1 	 2022-03-27 17:24
CREATE TABLE IF NOT EXISTS downloads
(
    hash TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    url TEXT NOT NULL,
    failed INTEGER DEFAULT 0,
    completed INTEGER DEFAULT 0,
    retries INTEGER DEFAULT 0,
    headers TEXT DEFAULT '{}',
    creation_date datetime not null,
    completion_date datetime
);
