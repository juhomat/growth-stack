# Framework Hexagonal

A Python 3.12 hexagonal architecture framework that provides a clean,
maintainable architecture for building Python applications.

The framework follows the Ports and Adapters (Hexagonal Architecture) pattern,
making it easy to plug in different adapters for different capabilities without
changing the core application logic.

## Features

- **Hexagonal Architecture**: Clean separation of concerns with ports and adapters
- **Integrated AI**: Ready-to-use OpenAI text and image generation
- **Web Capabilities**: Search, browsing, and screenshots
- **Database Integration**: SQLAlchemy-based persistence
- **HTTP API**: FastAPI integration
- **CLI Interface**: Command-line interface for all features
- **Streaming**: First-class support for streaming AI responses
- **Clean Architecture**: Clear separation of concerns with Ports and Adapters pattern
- **Extensible**: Easy to add new capabilities by plugging in new adapters
- **Async I/O**: All I/O operations are async for maximum performance
- **Type Hints**: Comprehensive type annotations throughout the codebase
- **Modular**: Use only the capabilities you need via optional dependencies
- **Dependency Injection**: Container for easy testing and swapping implementations
- **Various Adapters**:
  - **OpenAI**: GPT models for text generation and analysis
  - **DALL-E**: Image generation
  - **Tavily**: Web search
  - **HTTP Client**: Web page fetching
  - **Playwright**: Web screenshots
  - **SQLAlchemy**: Database access
- **Streaming Support**: Real-time responses
- **Helper Utilities**: For common tasks

## Current Capabilities

1. **Text AI** (chat/analysis) — default OpenAI adapter with async streaming
2. **Image AI** — default OpenAI Images adapter
3. **Web Search** — default Tavily adapter
4. **Web Fetcher + Scraper** — async HTML download + BeautifulSoup parsing
5. **Screenshotter** — full-page PNG using Playwright async API
6. **Database Gateway** — SQLAlchemy 2.x async (SQLite by default)

## Installation

Install the package with pip:

```bash
# Install core package
pip install framework_hexagonal

# Install with specific capabilities
pip install framework_hexagonal[openai]     # For OpenAI capabilities
pip install framework_hexagonal[web]        # For web fetching capabilities
pip install framework_hexagonal[playwright] # For screenshot capabilities

# Or install everything
pip install framework_hexagonal[all]
```

## Quick Start

```python
import asyncio
import os
from framework_hexagonal import container
from framework_hexagonal.core.ports import TextAI
from framework_hexagonal.adapters.outbound.openai_text import OpenAITextAdapter

# Register the OpenAI adapter
container.register(
    TextAI,
    OpenAITextAdapter(api_key=os.environ.get("OPENAI_API_KEY"))
)

async def main():
    # Get the registered adapter
    text_ai = container.get(TextAI)
    
    # Use the adapter
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, who are you?"}
    ]
    
    # Stream response chunks
    async for chunk in text_ai.chat(messages):
        print(chunk, end="", flush=True)
    print()

if __name__ == "__main__":
    asyncio.run(main())
```

## Example FastAPI Application

The package includes an example FastAPI application that demonstrates how to use
all capabilities. To run it:

```bash
# Install dependencies
pip install -e .[all]

# Set necessary API keys
export OPENAI_API_KEY=your_openai_key_here

# Run the FastAPI app
uvicorn framework_hexagonal.examples.fastapi_app.main:app --reload
```

Visit `http://localhost:8000` in your browser to see the API documentation.

## Architecture

The framework follows a hexagonal architecture with the following components:

- **Core**: The business logic and domain models
  - **Ports**: Interfaces that define capabilities
  - **Domain**: Value objects and domain models
  - **Container**: Dependency injection container

- **Adapters**: Implementations of the ports
  - **Outbound**: Adapters for external services

## Extending the Framework

To add a new capability:

1. Define a new port interface in `framework_hexagonal/core/ports/`
2. Create a new adapter implementation in `framework_hexagonal/adapters/outbound/`
3. Register the adapter in your application using the container

Example:

```python
# New port interface
class PDFParser(Protocol):
    async def parse(self, pdf_data: bytes) -> str:
        ...

# New adapter implementation
class PyPDFPDFParserAdapter:
    async def parse(self, pdf_data: bytes) -> str:
        # Implementation details...
        return text

# Register in your application
container.register(PDFParser, PyPDFPDFParserAdapter())
```

## Development

```bash
# Clone the repository
git clone https://github.com/your-username/framework-hexagonal.git
cd framework-hexagonal

# Install development dependencies
pip install -e .[all]

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy framework_hexagonal
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Examples

The framework includes several examples:

- **FastAPI Example**: Shows how to use all adapters in a FastAPI application with REST endpoints.
- **Streaming Example**: Demonstrates how to use the streaming utilities for real-time responses.
- **Demo Application**: A complete web application with UI for all features.

## Streaming

The framework provides utilities to easily implement streaming responses in FastAPI applications. For detailed documentation on streaming, see [Streaming Utilities](framework_hexagonal/utils/streaming/README.md).

### Modules

- `framework_hexagonal/core`: Core domain logic and interfaces (ports)
- `framework_hexagonal/adapters`: Implementation of the interfaces (adapters)
- `framework_hexagonal/config`: Configuration management
- `framework_hexagonal/utils`: Utility functions and helpers
  - `streaming`: Utilities for streaming responses in FastAPI
- `framework_hexagonal/examples`: Example applications using the framework
- `application`: A full demo application showcasing all features 