from __future__ import annotations

from dataclasses import dataclass

from .config import Settings


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str


class SearchError(RuntimeError):
    pass


def search_web(query: str, *, settings: Settings | None = None, max_results: int | None = None) -> list[SearchResult]:
    settings = settings or Settings()
    limit = max(1, min(max_results or settings.search_max_results, 10))

    try:
        from ddgs import DDGS
    except ImportError as exc:
        raise SearchError("Missing dependency: install requirements.txt to enable web search.") from exc

    try:
        with DDGS(timeout=20) as ddgs:
            raw_results = list(
                ddgs.text(
                    query,
                    region=settings.search_region,
                    max_results=limit,
                )
            )
    except Exception as exc:
        raise SearchError(f"Web search failed: {exc}") from exc

    results: list[SearchResult] = []
    for item in raw_results:
        title = str(item.get("title") or "").strip()
        url = str(item.get("href") or item.get("url") or "").strip()
        snippet = str(item.get("body") or item.get("snippet") or "").strip()
        if title and url:
            results.append(SearchResult(title=title, url=url, snippet=snippet))
    return results


def render_search_context(query: str, results: list[SearchResult]) -> str:
    if not results:
        return f"WEB SEARCH\nQuery: {query}\nNo results found."

    lines = [
        "WEB SEARCH CONTEXT",
        f"Query: {query}",
        "Use these results as evidence and cite URLs in the answer.",
    ]
    for index, result in enumerate(results, start=1):
        lines.append("")
        lines.append(f"[{index}] {result.title}")
        lines.append(f"URL: {result.url}")
        if result.snippet:
            lines.append(f"Snippet: {result.snippet}")
    return "\n".join(lines)
