"""AniWave integration slot; no undocumented scraping is implemented."""
from anizoro.providers.base import Provider, ProviderError

class AniWaveProvider(Provider):
    name = "aniwave"
    description = "AniWave provider slot (not configured)"

    def search(self, query: str):
        raise ProviderError("AniWave has no configured authorised API integration.")
