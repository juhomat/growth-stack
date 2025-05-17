"""Tests for port adapters."""
import pytest
import pytest_asyncio
from typing import List, Dict
from framework_hexagonal.core.ports import (
    TextAI,
    ImageAI,
    WebSearch,
    WebFetcher,
    Screenshotter,
    DBGateway,
)
from framework_hexagonal.tests.conftest import TestModel


@pytest.mark.asyncio
async def test_text_ai(container):
    """Test TextAI port."""
    text_ai = container.get(TextAI)
    
    # Test chat method
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
    ]
    
    chunks = []
    async for chunk in text_ai.chat(messages):
        chunks.append(chunk)
    
    assert len(chunks) > 0
    assert "".join(chunks) == "Hello, this is a test response"
    
    # Test analyze method
    analysis = await text_ai.analyze(
        "This is a test text to analyze.",
        "Summarize the given text."
    )
    
    assert "Analysis of text" in analysis
    assert "Summarize" in analysis


@pytest.mark.asyncio
async def test_image_ai(container):
    """Test ImageAI port."""
    image_ai = container.get(ImageAI)
    
    # Test generate_image method
    image_url = await image_ai.generate_image(
        "A beautiful sunset over mountains"
    )
    
    assert isinstance(image_url, str)
    assert image_url.startswith("https://")


@pytest.mark.asyncio
async def test_web_search(container):
    """Test WebSearch port."""
    web_search = container.get(WebSearch)
    
    # Test search method
    results = await web_search.search("test query", max_results=2)
    
    assert len(results) == 2
    assert results[0].title == "Result 1 for test query"
    assert results[0].url == "https://example.com/result1"
    assert results[0].snippet == "This is a snippet for result 1."


@pytest.mark.asyncio
async def test_web_fetcher(container):
    """Test WebFetcher port."""
    web_fetcher = container.get(WebFetcher)
    
    # Test fetch method
    page = await web_fetcher.fetch("https://example.com")
    
    assert page.url == "https://example.com"
    assert page.status_code == 200
    assert "<h1>Example Page for https://example.com</h1>" in page.html
    assert page.soup is not None
    
    # Test get_text method
    text = await web_fetcher.get_text("https://example.com", selector="h1")
    
    assert "Text content from https://example.com" in text


@pytest.mark.asyncio
async def test_screenshotter(container):
    """Test Screenshotter port."""
    screenshotter = container.get(Screenshotter)
    
    # Test capture method
    screenshot = await screenshotter.capture("https://example.com")
    
    assert screenshot == b"MOCK_SCREENSHOT_DATA"
    
    # Test capture_element method
    element_screenshot = await screenshotter.capture_element(
        "https://example.com", 
        selector="#header"
    )
    
    assert element_screenshot == b"MOCK_ELEMENT_SCREENSHOT_DATA"


@pytest.mark.asyncio
async def test_db_gateway(container, db_gateway):
    """Test DBGateway port."""
    # Test create method
    test_record = await db_gateway.create(
        TestModel,
        {"name": "Test Record"}
    )
    
    assert test_record.id is not None
    assert test_record.name == "Test Record"
    
    # Test get_by_id method
    retrieved = await db_gateway.get_by_id(TestModel, test_record.id)
    
    assert retrieved is not None
    assert retrieved.id == test_record.id
    assert retrieved.name == "Test Record"
    
    # Test update method
    updated = await db_gateway.update(
        TestModel,
        test_record.id,
        {"name": "Updated Record"}
    )
    
    assert updated is not None
    assert updated.id == test_record.id
    assert updated.name == "Updated Record"
    
    # Test delete method
    deleted = await db_gateway.delete(TestModel, test_record.id)
    
    assert deleted is True
    
    # Verify record is deleted
    not_found = await db_gateway.get_by_id(TestModel, test_record.id)
    
    assert not_found is None 