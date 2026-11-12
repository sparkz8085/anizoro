"""Launch local or authorised playback targets with MPV."""
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

class PlayerError(RuntimeError):
    pass

def play(target: str) -> int:
    if not target.strip():
        raise PlayerError("Playback target cannot be empty.")
    parsed = urlparse(target)
    is_url = parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    is_file = Path(target).expanduser().is_file()
    if not (is_url or is_file):
        raise PlayerError("Target must be an existing local file or an authorised HTTP(S) URL.")
    executable = shutil.which("mpv")
    if not executable:
        raise PlayerError("MPV was not found. Install it with: sudo dnf install mpv")
    return subprocess.run([executable, "--", target], check=False).returncode
