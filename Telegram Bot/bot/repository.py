import time, sqlite3, os

class SeenRepo:
    """
    Uses an on-disk SQLite DB to persist seen alerts across restarts.
    """
    def __init__(self, db_path="seen.db", ttl_seconds=6*3600):
        self.ttl = ttl_seconds
        self.db_path = db_path
        init = not os.path.exists(db_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        if init:
            self.conn.execute("CREATE TABLE seen(key TEXT PRIMARY KEY, ts INTEGER)")
            self.conn.commit()

    def _purge(self):
        cutoff = int(time.time()) - self.ttl
        self.conn.execute("DELETE FROM seen WHERE ts < ?", (cutoff,))
        self.conn.commit()

    def already_seen(self, key: str) -> bool:
        self._purge()
        r = self.conn.execute("SELECT 1 FROM seen WHERE key = ?", (key,)).fetchone()
        return bool(r)

    def mark_seen(self, key: str):
        now = int(time.time())
        self.conn.execute("INSERT OR REPLACE INTO seen(key, ts) VALUES (?, ?)", (key, now))
        self.conn.commit()
