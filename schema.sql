CREATE TABLE IF NOT EXISTS downloads
(
    hash TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    completed INTEGER DEFAULT 0
);
