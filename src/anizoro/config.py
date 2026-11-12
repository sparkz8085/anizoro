"""Application paths and defaults."""
from pathlib import Path

APP_DIR = Path.home() / ".local" / "share" / "anizoro"
DB_PATH = APP_DIR / "anizoro.db"

def ensure_app_dir() -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
