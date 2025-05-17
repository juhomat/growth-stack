"""Playwright adapter for Screenshotter port."""
from typing import Optional, Any, Literal, Dict, Union
from pathlib import Path
import os
import asyncio
from playwright.async_api import async_playwright, Browser, Page, Playwright
from ...core.ports.screenshotter import Screenshotter


class PlaywrightScreenshotterAdapter:
    """Playwright implementation of the Screenshotter port."""

    def __init__(
        self,
        browser_type: str = "chromium",
        headless: bool = True,
        default_viewport_size: Dict[str, int] = None,
    ):
        """
        Initialize the Playwright screenshotter adapter.

        Args:
            browser_type: Browser to use ('chromium', 'firefox', or 'webkit')
            headless: Whether to run the browser in headless mode
            default_viewport_size: Default viewport size
        """
        self.browser_type = browser_type
        self.headless = headless
        self.default_viewport_size = default_viewport_size or {"width": 1280, "height": 800}
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None

    async def _ensure_browser(self) -> Browser:
        """
        Ensure browser is launched.

        Returns:
            Playwright browser instance
        """
        if self._browser is None or not self._browser.is_connected():
            if self._playwright is None:
                self._playwright = await async_playwright().start()
            
            browser_types = {
                "chromium": self._playwright.chromium,
                "firefox": self._playwright.firefox,
                "webkit": self._playwright.webkit,
            }
            
            launcher = browser_types.get(self.browser_type, self._playwright.chromium)
            self._browser = await launcher.launch(headless=self.headless)
            
        return self._browser

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
        browser = await self._ensure_browser()
        
        # Use context to set viewport size
        context = await browser.new_context(
            viewport={"width": width, "height": height}
        )
        
        try:
            page = await context.new_page()
            
            # Navigate to the URL
            await page.goto(url, wait_until=wait_until, timeout=timeout * 1000)
            
            # Allow extra time for any animations or dynamic content
            if kwargs.get("wait_after_load"):
                await asyncio.sleep(kwargs["wait_after_load"])
            
            # Take the screenshot
            screenshot_options = {
                "full_page": full_page,
                "type": format,
                **{k: v for k, v in kwargs.items() if k not in ["wait_after_load"]},
            }
            
            screenshot_bytes = await page.screenshot(**screenshot_options)
            
            # Save to file if output path is provided
            if output_path:
                path = Path(output_path)
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, "wb") as f:
                    f.write(screenshot_bytes)
            
            return screenshot_bytes
        finally:
            await context.close()

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
        browser = await self._ensure_browser()
        context = await browser.new_context(
            viewport=kwargs.get("viewport", self.default_viewport_size)
        )
        
        try:
            page = await context.new_page()
            
            # Navigate to the URL
            wait_until = kwargs.get("wait_until", "networkidle")
            timeout = kwargs.get("timeout", 30.0) * 1000
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            
            # Wait for the element to be visible
            element = await page.wait_for_selector(selector, timeout=timeout)
            if not element:
                raise ValueError(f"Element with selector '{selector}' not found")
            
            # Take the screenshot of the element
            screenshot_options = {"type": format}
            screenshot_bytes = await element.screenshot(**screenshot_options)
            
            # Save to file if output path is provided
            if output_path:
                path = Path(output_path)
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, "wb") as f:
                    f.write(screenshot_bytes)
            
            return screenshot_bytes
        finally:
            await context.close()

    async def close(self) -> None:
        """Close browser and playwright resources."""
        if self._browser:
            await self._browser.close()
            self._browser = None
        
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None 