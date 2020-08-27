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
