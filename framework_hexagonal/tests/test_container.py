"""Tests for the container functionality."""
import pytest
from framework_hexagonal.core.container import Container
from framework_hexagonal.core.ports import TextAI, ImageAI, WebSearch


class MockAdapter:
    """Mock adapter for testing."""
    pass


def test_container_register_and_get():
    """Test registering and retrieving adapters from container."""
    container = Container()
    mock_adapter = MockAdapter()
    
    # Register adapter
    container.register(TextAI, mock_adapter)
    
    # Get adapter
    adapter = container.get(TextAI)
    
    assert adapter is mock_adapter
    assert container.has(TextAI)
    assert not container.has(ImageAI)


def test_container_get_missing():
    """Test getting missing adapter from container."""
    container = Container()
    
    with pytest.raises(KeyError):
        container.get(WebSearch)


def test_container_has():
    """Test checking if adapter exists in container."""
    container = Container()
    mock_adapter = MockAdapter()
    
    assert not container.has(TextAI)
    
    container.register(TextAI, mock_adapter)
    
    assert container.has(TextAI)


def test_container_register_replace():
    """Test replacing adapter in container."""
    container = Container()
    mock_adapter1 = MockAdapter()
    mock_adapter2 = MockAdapter()
    
    container.register(TextAI, mock_adapter1)
    adapter1 = container.get(TextAI)
    assert adapter1 is mock_adapter1
    
    container.register(TextAI, mock_adapter2)
    adapter2 = container.get(TextAI)
    assert adapter2 is mock_adapter2
    assert adapter2 is not adapter1 