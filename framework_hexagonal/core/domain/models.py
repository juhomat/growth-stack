"""Domain model classes for the framework."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum


class ContentType(str, Enum):
    """Enum for content types."""
    
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    PDF = "pdf"
    HTML = "html"
    JSON = "json"
    OTHER = "other"


@dataclass
class Content:
    """Base content data class."""
    
    type: ContentType
    data: Any
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class TextContent(Content):
    """Text content data class."""
    
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(ContentType.TEXT, text, metadata)
        
    @property
    def text(self) -> str:
        """Get the text data."""
        return self.data


@dataclass
class ImageContent(Content):
    """Image content data class."""
    
    def __init__(
        self,
        data: Union[bytes, str],
        format: str = "png",
        metadata: Optional[Dict[str, Any]] = None
    ):
        meta = metadata or {}
        meta["format"] = format
        super().__init__(ContentType.IMAGE, data, meta)
    
    @property
    def format(self) -> str:
        """Get the image format."""
        return self.metadata.get("format", "png") if self.metadata else "png"


@dataclass
class WebResource:
    """Web resource data class."""
    
    url: str
    content: Optional[Content] = None
    last_accessed: Optional[datetime] = None
    headers: Optional[Dict[str, str]] = None
    status_code: Optional[int] = None 