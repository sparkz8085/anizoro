# Anizoro

**Anizoro** is a terminal-first anime discovery and playback launcher for Linux. Its design is inspired by the simplicity of `ani-cli`: search, choose a title, choose an episode/source when available, and hand supported media to MPV.

This repository contains a modular provider architecture. The AniLili and AniWave provider modules are **integration placeholders**. They do not scrape sites, extract unauthorised streams, bypass access controls, or claim to have working playback integration. They can be connected later where a provider offers a documented and authorised integration.

## Features

- Terminal interface built with Typer and Rich.
- Provider registry with separate AniLili and AniWave adapter slots.
- Working AniList catalogue search and title details.
- SQLite watchlist and playback-history foundation.
- MPV launcher for local files and authorised media URLs.
- Fedora-friendly Python packaging.

## Fedora installation

```bash
sudo dnf install -y python3 python3-pip mpv fzf
git clone https://github.com/sparkz8085/anizoro.git
cd anizoro
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

## Commands

```bash
anizoro --help
anizoro providers
anizoro search "Death Note"
anizoro search "Death Note" --provider anilist
anizoro watchlist
anizoro add 1535 "Death Note" --url https://anilist.co/anime/1535
anizoro remove 1535
anizoro play-media "/path/to/your/video.mkv"
```

The `anilili` and `aniwave` adapters currently report that no authorised catalogue/playback integration is configured. This is intentional; no working source integration is implied.

## Local data

The SQLite database is stored at `~/.local/share/anizoro/anizoro.db`. AniList metadata search uses its public GraphQL endpoint and does not require an API key.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## Project layout

```text
src/anizoro/
├── cli.py
├── config.py
├── database.py
├── models.py
├── player.py
└── providers/
    ├── __init__.py
    ├── base.py
    ├── registry.py
    ├── anilist.py
    ├── anilili.py
    └── aniwave.py
tests/
└── test_database.py
```

## Provider and playback note

Anizoro is a metadata client and playback launcher, not a host for third-party video. Use local media or sources you are authorised to access. Provider adapters must follow provider terms, applicable law, and documented access methods.

## License

See [LICENSE](LICENSE).
