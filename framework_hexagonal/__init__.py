"""
Framework Hexagonal: A hexagonal architecture framework for Python applications.

This framework provides a clean, maintainable architecture following
the Ports and Adapters / Hexagonal Architecture pattern.
"""

from .core.container import container
from .core.ports import (
    TextAI,
    ImageAI,
    WebSearch,
    SearchResult,
    WebFetcher,
    FetchedPage,
    Screenshotter,
    DBGateway,
)
from .core.domain import (
    Content,
    ContentType,
    TextContent,
    ImageContent,
    WebResource,
)

# Import streaming utils
from framework_hexagonal.utils.streaming import create_streaming_endpoint, get_streaming_js, stream_response, get_streaming_html

__version__ = "0.1.0"

__all__ = [
    # Container
    "container",
    
    # Ports
    "TextAI",
    "ImageAI",
    "WebSearch",
    "SearchResult",
    "WebFetcher",
    "FetchedPage",
    "Screenshotter",
    "DBGateway",
    
    # Domain
    "Content",
    "ContentType",
    "TextContent",
    "ImageContent",
    "WebResource",
    
    # Streaming
    "create_streaming_endpoint",
    "get_streaming_js",
    "stream_response",
    "get_streaming_html",
] 