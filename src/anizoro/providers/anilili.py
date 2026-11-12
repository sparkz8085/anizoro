"""AniLili integration slot; no undocumented scraping is implemented."""
from anizoro.providers.base import Provider, ProviderError

class AniLiliProvider(Provider):
    name = "anilili"
    description = "AniLili provider slot (not configured)"

    def search(self, query: str):
        raise ProviderError("AniLili has no configured authorised API integration.")
