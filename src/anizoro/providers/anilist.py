"""AniList public GraphQL catalogue provider (metadata only)."""
import httpx
from anizoro.models import Anime
from anizoro.providers.base import Provider, ProviderError

API_URL = "https://graphql.anilist.co"
QUERY = """query ($search: String) {
  Page(perPage: 10) {
    media(search: $search, type: ANIME, sort: SEARCH_MATCH) {
      id siteUrl description(asHtml: false) coverImage { large }
      title { romaji english native }
    }
  }
}"""

class AniListProvider(Provider):
    name = "anilist"
    description = "Public anime metadata catalogue"

    def search(self, query: str) -> list[Anime]:
        try:
            response = httpx.post(API_URL, json={"query": QUERY, "variables": {"search": query}},
                                  timeout=20.0, headers={"User-Agent": "Anizoro/0.2.0"})
            response.raise_for_status()
            payload = response.json()
            if payload.get("errors"):
                raise ProviderError("AniList returned a GraphQL error.")
            media = payload.get("data", {}).get("Page", {}).get("media", [])
            results = []
            for item in media:
                titles = item.get("title") or {}
                cover = item.get("coverImage") or {}
                results.append(Anime(
                    id=str(item["id"]),
                    title=titles.get("english") or titles.get("romaji") or titles.get("native") or "Untitled",
                    url=item.get("siteUrl"), synopsis=item.get("description"),
                    cover_url=cover.get("large"), provider=self.name))
            return results
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            raise ProviderError(f"AniList request failed: {exc}") from exc
