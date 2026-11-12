"""SQLite store for watchlist and playback progress."""
import sqlite3
from pathlib import Path
from anizoro.config import DB_PATH

class Database:
    def __init__(self, path: Path | str = DB_PATH):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS watchlist (
                anime_id TEXT PRIMARY KEY, title TEXT NOT NULL, url TEXT,
                status TEXT NOT NULL DEFAULT 'Plan to Watch',
                added_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
            db.execute("""CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT, anime_id TEXT NOT NULL,
                episode_id TEXT NOT NULL, position_seconds REAL NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(anime_id, episode_id))""")

    def _connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def add(self, anime_id: str, title: str, url: str | None = None) -> None:
        with self._connect() as db:
            db.execute("""INSERT INTO watchlist(anime_id,title,url) VALUES(?,?,?)
                ON CONFLICT(anime_id) DO UPDATE SET
                title=excluded.title,url=excluded.url""", (str(anime_id), title, url))

    def remove(self, anime_id: str) -> bool:
        with self._connect() as db:
            cur = db.execute("DELETE FROM watchlist WHERE anime_id=?", (str(anime_id),))
            return cur.rowcount > 0

    def list_watchlist(self) -> list[dict]:
        with self._connect() as db:
            rows = db.execute("SELECT anime_id,title,url,status,added_at FROM watchlist ORDER BY added_at DESC").fetchall()
            return [dict(row) for row in rows]

    def save_progress(self, anime_id: str, episode_id: str, position_seconds: float) -> None:
        with self._connect() as db:
            db.execute("""INSERT INTO history(anime_id,episode_id,position_seconds)
                VALUES(?,?,?) ON CONFLICT(anime_id,episode_id) DO UPDATE SET
                position_seconds=excluded.position_seconds,updated_at=CURRENT_TIMESTAMP""",
                (str(anime_id), str(episode_id), max(0.0, position_seconds)))
