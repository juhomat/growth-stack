"""HTTPX adapter for WebFetcher port."""
from typing import Dict, Optional, Any
import httpx
from bs4 import BeautifulSoup
from ...core.ports.web_fetcher import WebFetcher, FetchedPage


class HttpxWebFetcherAdapter:
    """HTTPX implementation of the WebFetcher port."""

    def __init__(
        self,
        default_headers: Optional[Dict[str, str]] = None,
        default_timeout: float = 30.0,
        follow_redirects: bool = True,
        parser: str = "html.parser",
    ):
        """
        Initialize the HTTPX web fetcher adapter.

        Args:
            default_headers: Default headers to include in requests
            default_timeout: Default timeout for requests in seconds
            follow_redirects: Whether to follow HTTP redirects
            parser: BeautifulSoup parser to use
        """
        self.default_headers = default_headers or {
            "User-Agent": "framework-hexagonal/0.1.0 (+https://github.com/framework-hexagonal)"
        }
        self.default_timeout = default_timeout
        self.follow_redirects = follow_redirects
        self.parser = parser

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
            **kwargs: Additional request parameters

        Returns:
            FetchedPage containing html content and parsed BeautifulSoup
        """
        request_headers = {**self.default_headers}
        if headers:
            request_headers.update(headers)
            
        request_timeout = httpx.Timeout(timeout)
        
        async with httpx.AsyncClient(
            follow_redirects=self.follow_redirects,
            timeout=request_timeout,
        ) as client:
            response = await client.get(url, headers=request_headers, **kwargs)
            response.raise_for_status()
            
            html = response.text
            soup = BeautifulSoup(html, self.parser)
            
            return FetchedPage(
                url=str(response.url),
                status_code=response.status_code,
                html=html,
                soup=soup,
                headers=dict(response.headers),
            )

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
            **kwargs: Additional request parameters

        Returns:
            Extracted text content
        """
        page = await self.fetch(url, **kwargs)
        
        if selector:
            elements = page.soup.select(selector)
            return " ".join(element.get_text(strip=True) for element in elements)
        else:
            return page.soup.get_text(strip=True) 