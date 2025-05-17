# Hexagonal Framework Demo Application

This is a demonstration application showcasing all the features of the hexagonal framework. The application provides a simple web interface to test all the adapters implemented in the framework.

## Features

This demo application includes UI interfaces for testing:

- **Text AI (OpenAI)**: Chat with AI and text analysis
- **Image AI (DALL-E)**: Generate images from text prompts
- **Web Search (Tavily)**: Search the web for information
- **Web Fetcher (HTTPX)**: Fetch and parse web pages
- **Web Screenshots (Playwright)**: Take screenshots of web pages
- **Database (SQLAlchemy)**: Integrated but not exposed in UI
- **Streaming**: Real-time streaming responses using the framework's utilities

## Installation

The demo application uses the same dependencies as the main framework. Make sure you have installed all the required dependencies:

```bash
pip install -e .
```

## Configuration

The application uses environment variables for configuration. Make sure you have a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
DATABASE_URL=sqlite:///./test.db  # Or your preferred database URL
```

## Running the Application

To run the application:

```bash
python -m application.main
```

The application will be available at http://127.0.0.1:8000.

## Usage

1. Open your browser and navigate to http://127.0.0.1:8000
2. Use the different sections of the web interface to test various features:
   - Chat with AI: Send messages to the AI and see responses
   - Text Analysis: Analyze text with custom prompts
   - Image Generation: Generate images using DALL-E
   - Web Search: Search the web using Tavily
   - Web Fetcher: Fetch content from web pages
   - Web Screenshots: Take screenshots of web pages

## Adapters Used

This demo uses the following adapters from the framework:

- `OpenAITextAdapter`: For text generation and analysis
- `OpenAIImageAdapter`: For image generation
- `TavilySearchAdapter`: For web search
- `HttpxWebFetcherAdapter`: For fetching web content
- `PlaywrightScreenshotterAdapter`: For taking web screenshots
- `SQLAlchemyDBAdapter`: For database operations

## Architecture

The application follows the hexagonal architecture pattern:

- **Ports**: Defined in the framework core (TextAI, ImageAI, etc.)
- **Adapters**: Implementation of the ports (OpenAITextAdapter, etc.)
- **Application Logic**: In the FastAPI routes
- **UI**: HTML templates using Jinja2 

## Streaming

The application demonstrates how to use the framework's streaming utilities to create real-time, responsive interfaces. The streaming implementation consists of:

1. **Backend**: 
   - Uses `framework_hexagonal.utils.streaming` utilities
   - The `/chat-stream` endpoint processes messages and returns a streaming response
   - The framework's `stream_response()` function handles the response formatting

2. **Frontend**:
   - HTML components are generated with `get_streaming_html()`
   - JavaScript handling is generated with `get_streaming_js()`
   - These utilities are passed to the template from the main route

Example implementation:

```python
# In your FastAPI application:
from framework_hexagonal.utils.streaming import get_streaming_html, get_streaming_js, stream_response

# Add the streaming endpoint
@app.post("/chat-stream")
async def chat_stream(message: str = Form(...), text_ai = Depends(get_text_ai)):
    # Process the message
    async def generate():
        async for chunk in text_ai.chat(messages=[{"role": "user", "content": message}]):
            yield chunk
    return stream_response(generate())

# Pass the streaming utilities to the template
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "get_streaming_html": get_streaming_html,
            "get_streaming_js": get_streaming_js,
        },
    )
```

```html
<!-- In your HTML template: -->
<!-- Add the HTML for the streaming form -->
{{ get_streaming_html("streaming", "Enter your message") | safe }}

<!-- Add the JavaScript for handling streaming -->
{{ get_streaming_js("streaming", "/chat-stream") | safe }}
```

This approach provides a clean separation between the UI components and the functionality, making it easy to add streaming to any application using the framework. 