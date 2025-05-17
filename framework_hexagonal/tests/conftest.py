"""Test configuration with fixtures."""
import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Dict, List, Optional, Any, Type, cast, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, select

from framework_hexagonal.core.container import Container
from framework_hexagonal.core.ports import (
    TextAI,
    ImageAI,
    WebSearch,
    SearchResult,
    WebFetcher,
    FetchedPage,
    Screenshotter,
    DBGateway,
)

T = TypeVar('T')


# Stub adapter implementations for testing
class StubTextAIAdapter:
    """Stub implementation of TextAI for testing."""
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        """Return mock chat response chunks."""
        chunks = ["Hello", ", ", "this", " ", "is", " ", "a", " ", "test", " ", "response"]
        for chunk in chunks:
            yield chunk
    
    async def analyze(
        self,
        text: str,
        prompt: str,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Return mock analysis response."""
        return f"Analysis of text: {text[:10]}... based on prompt: {prompt[:10]}..."


class StubImageAIAdapter:
    """Stub implementation of ImageAI for testing."""
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1,
        **kwargs: Any,
    ) -> str:
        """Return mock image URL."""
        return "https://example.com/image.png"
    
    async def edit_image(
        self,
        image: bytes,
        mask: Optional[bytes] = None,
        prompt: str = "",
        size: str = "1024x1024",
        **kwargs: Any,
    ) -> str:
        """Return mock edited image URL."""
        return "https://example.com/edited_image.png"


class StubWebSearchAdapter:
    """Stub implementation of WebSearch for testing."""
    
    async def search(
        self,
        query: str,
        max_results: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[SearchResult]:
        """Return mock search results."""
        return [
            SearchResult(
                title=f"Result 1 for {query}",
                url="https://example.com/result1",
                snippet="This is a snippet for result 1.",
            ),
            SearchResult(
                title=f"Result 2 for {query}",
                url="https://example.com/result2",
                snippet="This is a snippet for result 2.",
            ),
        ][:max_results]


class StubWebFetcherAdapter:
    """Stub implementation of WebFetcher for testing."""
    
    async def fetch(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
        **kwargs: Any,
    ) -> FetchedPage:
        """Return mock fetched page."""
        from bs4 import BeautifulSoup
        html = f"<html><body><h1>Example Page for {url}</h1><p>This is a test page.</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        return FetchedPage(
            url=url,
            status_code=200,
            html=html,
            soup=soup,
            headers={"Content-Type": "text/html"},
        )
    
    async def get_text(
        self,
        url: str,
        selector: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Return mock text content."""
        return f"Text content from {url}" + (f" with selector {selector}" if selector else "")


class StubScreenshotterAdapter:
    """Stub implementation of Screenshotter for testing."""
    
    async def capture(
        self,
        url: str,
        output_path: Optional[str] = None,
        full_page: bool = True,
        width: int = 1280,
        height: int = 800,
        format: str = "png",
        wait_until: str = "networkidle",
        timeout: float = 30.0,
        **kwargs: Any,
    ) -> bytes:
        """Return mock screenshot bytes."""
        return b"MOCK_SCREENSHOT_DATA"
    
    async def capture_element(
        self,
        url: str,
        selector: str,
        output_path: Optional[str] = None,
        format: str = "png",
        **kwargs: Any,
    ) -> bytes:
        """Return mock element screenshot bytes."""
        return b"MOCK_ELEMENT_SCREENSHOT_DATA"


# In-memory SQLite for testing
Base = declarative_base()


class TestModel(Base):
    """Test model for database testing."""
    
    __tablename__ = "test_model"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class MockAsyncSession:
    """Mock AsyncSession that can be used with async with."""
    
    def __init__(self, instance_data=None):
        """Initialize with instance data for mocking."""
        self.instance_data = instance_data or {}
        self.committed = False
        self.closed = False
        
    async def __aenter__(self):
        """Enter the async context."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context."""
        await self.close()
        
    async def commit(self):
        """Mock commit."""
        self.committed = True
        
    async def close(self):
        """Mock close."""
        self.closed = True
        
    async def refresh(self, instance):
        """Mock refresh by setting a fake ID if not present."""
        if hasattr(instance, 'id') and instance.id is None:
            instance.id = 1
        
    def add(self, instance):
        """Mock add to session."""
        pass


class StubDBGatewayAdapter:
    """Stub implementation of DBGateway for testing."""
    
    def __init__(self):
        """Initialize in-memory SQLite engine."""
        self.engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            echo=False,
        )
        self._test_instances = {}
        self._next_id = 1
    
    async def initialize_db(self):
        """Create tables in the database."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_session(self) -> MockAsyncSession:
        """Return a mock database session that works with async with."""
        return MockAsyncSession()
    
    async def execute(
        self,
        statement: Any,
        **kwargs: Any,
    ) -> Any:
        """Execute a SQL statement."""
        # Just return a mock result
        class MockResult:
            def __init__(self):
                self.data = []
                
            def all(self):
                return self.data
                
            def scalar_one_or_none(self):
                return None
        
        return MockResult()
    
    async def get_by_id(
        self,
        model: Type[T],
        id: Any,
        **kwargs: Any,
    ) -> Optional[T]:
        """Get a record by ID."""
        key = f"{model.__name__}_{id}"
        return self._test_instances.get(key)
    
    async def create(
        self,
        model: Type[T],
        data: Dict[str, Any],
        **kwargs: Any,
    ) -> T:
        """Create a new record."""
        instance = model(**data)
        instance.id = self._next_id
        self._next_id += 1
        
        key = f"{model.__name__}_{instance.id}"
        self._test_instances[key] = instance
        
        return instance
    
    async def update(
        self,
        model: Type[T],
        id: Any,
        data: Dict[str, Any],
        **kwargs: Any,
    ) -> Optional[T]:
        """Update an existing record."""
        instance = await self.get_by_id(model, id)
        if instance is None:
            return None
        
        for key, value in data.items():
            setattr(instance, key, value)
        
        key = f"{model.__name__}_{id}"
        self._test_instances[key] = instance
        
        return instance
    
    async def delete(
        self,
        model: Type[T],
        id: Any,
        **kwargs: Any,
    ) -> bool:
        """Delete a record."""
        key = f"{model.__name__}_{id}"
        if key in self._test_instances:
            del self._test_instances[key]
            return True
        return False


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def container():
    """Create a test container with stub adapters."""
    container = Container()
    
    # Register stub adapters
    container.register(TextAI, StubTextAIAdapter())
    container.register(ImageAI, StubImageAIAdapter())
    container.register(WebSearch, StubWebSearchAdapter())
    container.register(WebFetcher, StubWebFetcherAdapter())
    container.register(Screenshotter, StubScreenshotterAdapter())
    
    # Set up DB adapter
    db_adapter = StubDBGatewayAdapter()
    await db_adapter.initialize_db()
    container.register(DBGateway, db_adapter)
    
    yield container


@pytest_asyncio.fixture
async def db_gateway(container):
    """Get DB gateway from container."""
    return container.get(DBGateway)