"""WebSearch port for searching the internet."""
from typing import List, Dict, Any, Protocol, Optional


class SearchResult:
    """Data class for search results."""

    def __init__(
        self,
        title: str,
        url: str,
        snippet: str,
        content: Optional[str] = None,
    ):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.content = content

    def __repr__(self) -> str:
        return f"SearchResult(title='{self.title}', url='{self.url}')"


class WebSearch(Protocol):
    """Interface for web search capabilities."""

    async def search(
        self,
        query: str,
        max_results: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[SearchResult]:
        """
        Search the web and return results.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            filters: Optional filters like date range, region, etc.
            **kwargs: Additional provider-specific parameters

        Returns:
            List of search results
        """
        ... 