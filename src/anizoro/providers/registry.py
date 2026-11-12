"""Central provider registry."""
from anizoro.providers.anilist import AniListProvider
from anizoro.providers.anilili import AniLiliProvider
from anizoro.providers.aniwave import AniWaveProvider
from anizoro.providers.base import Provider

_PROVIDERS: dict[str, Provider] = {
    "anilist": AniListProvider(),
    "anilili": AniLiliProvider(),
    "aniwave": AniWaveProvider(),
}

def get_provider(name: str) -> Provider:
    key = name.strip().lower()
    try:
        return _PROVIDERS[key]
    except KeyError as exc:
        raise ValueError(f"Unknown provider '{name}'. Available: {', '.join(sorted(_PROVIDERS))}") from exc

def list_providers() -> list[Provider]:
    return list(_PROVIDERS.values())
