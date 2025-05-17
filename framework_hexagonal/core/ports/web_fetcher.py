"""WebFetcher port for downloading and parsing web pages."""
from typing import Dict, Optional, Protocol, Any, NamedTuple
from bs4 import BeautifulSoup


class FetchedPage(NamedTuple):
    """Data container for fetched web page content."""
    
    url: str
    status_code: int
    html: str
    soup: BeautifulSoup
    headers: Dict[str, str]


class WebFetcher(Protocol):
    """Interface for web page fetching and parsing capabilities."""

    async def fetch(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
        **kwargs: Any,
    ) -> FetchedPage:
        """
        Fetch a web page and return its parsed content.

        Args:
            url: The URL to fetch
            headers: Optional request headers
            timeout: Request timeout in seconds
            **kwargs: Additional provider-specific parameters

        Returns:
            FetchedPage containing html content and parsed BeautifulSoup
        """
        ...

    async def get_text(
        self,
        url: str,
        selector: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """
        Extract text from a web page, optionally filtering by CSS selector.

        Args:
            url: The URL to fetch
            selector: Optional CSS selector to filter content
            **kwargs: Additional provider-specific parameters

        Returns:
            Extracted text content
        """
        ... 