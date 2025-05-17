"""Screenshotter port for capturing screenshots of web pages."""
from typing import Optional, Protocol, Any, Literal, Dict, Union
from pathlib import Path


class Screenshotter(Protocol):
    """Interface for web page screenshot capabilities."""

    async def capture(
        self,
        url: str,
        output_path: Optional[Union[str, Path]] = None,
        full_page: bool = True,
        width: int = 1280,
        height: int = 800,
        format: Literal["png", "jpeg"] = "png",
        wait_until: Literal["load", "domcontentloaded", "networkidle"] = "networkidle",
        timeout: float = 30.0,
        **kwargs: Any,
    ) -> bytes:
        """
        Capture a screenshot of a web page.

        Args:
            url: The URL to screenshot
            output_path: Optional path to save the screenshot
            full_page: Whether to capture the full page or just the viewport
            width: Browser viewport width
            height: Browser viewport height
            format: Image format (png or jpeg)
            wait_until: Page load state to wait for
            timeout: Maximum time to wait for page load in seconds
            **kwargs: Additional provider-specific parameters

        Returns:
            Binary image data
        """
        ...

    async def capture_element(
        self,
        url: str,
        selector: str,
        output_path: Optional[Union[str, Path]] = None,
        format: Literal["png", "jpeg"] = "png",
        **kwargs: Any,
    ) -> bytes:
        """
        Capture a screenshot of a specific element on a web page.

        Args:
            url: The URL to screenshot
            selector: CSS selector for the element to capture
            output_path: Optional path to save the screenshot
            format: Image format (png or jpeg)
            **kwargs: Additional provider-specific parameters

        Returns:
            Binary image data
        """
        ... 