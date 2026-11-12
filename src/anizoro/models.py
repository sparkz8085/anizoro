"""Shared provider and catalogue models."""
from dataclasses import dataclass

@dataclass(slots=True)
class Anime:
    id: str
    title: str
    url: str | None = None
    synopsis: str | None = None
    cover_url: str | None = None
    provider: str = "unknown"

@dataclass(slots=True)
class Episode:
    id: str
    title: str
    number: int | None = None
    playback_url: str | None = None
    provider: str = "unknown"
