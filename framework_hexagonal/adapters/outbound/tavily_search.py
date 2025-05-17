"""Tavily adapter for WebSearch port."""
from typing import List, Dict, Any, Optional
import os
import json
import httpx
from ...core.ports.web_search import WebSearch, SearchResult


class TavilySearchAdapter:
    """Tavily implementation of the WebSearch port."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.tavily.com/search",
        timeout: float = 30.0,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
    ):
        """
        Initialize the Tavily search adapter.

        Args:
            api_key: Tavily API key (defaults to TAVILY_API_KEY env var)
            base_url: Base URL for the API
            timeout: Timeout for API calls in seconds
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
        """
        self.api_key = api_key or os.environ.get("TAVILY_API_KEY")
        self.base_url = base_url
        self.timeout = timeout
        self.include_domains = include_domains
        self.exclude_domains = exclude_domains
        
        # TODO: In actual implementation, validate API key

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
        # TODO: Implement actual Tavily API integration
        # This is a stub implementation for now
        
        # For demo purposes, return mock data
        mock_results = [
            SearchResult(
                title="Example Search Result 1",
                url="https://example.com/result1",
                snippet="This is a snippet from the first search result that matches the query.",
            ),
            SearchResult(
                title="Example Search Result 2",
                url="https://example.com/result2",
                snippet="Another snippet from the second search result with relevant information.",
            ),
        ]
        
        # Only return the requested number of results
        return mock_results[:max_results] 