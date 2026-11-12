"""Provider contract for documented, authorised integrations."""
from abc import ABC, abstractmethod
from anizoro.models import Anime, Episode

class ProviderError(RuntimeError):
    """Raised when a provider cannot complete a supported operation."""

class Provider(ABC):
    name: str
    description: str

    @abstractmethod
    def search(self, query: str) -> list[Anime]:
        """Search the provider catalogue."""

    def episodes(self, anime: Anime) -> list[Episode]:
        raise ProviderError(f"{self.name} has no configured episode integration.")

    def resolve(self, episode: Episode) -> str:
        if not episode.playback_url:
            raise ProviderError(f"{self.name} has no configured playback integration.")
        return episode.playback_url
