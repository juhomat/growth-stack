# Streaming Utilities

This module provides utilities for implementing HTTP streaming in FastAPI applications. The streaming functionality uses HTTP streaming (not WebSockets) to provide real-time responses from the server to the client.

## Installation

To use the streaming functionality, ensure you have the required dependencies:

```bash
# Install the framework with all dependencies
pip install -e .[all]

# Install required dependencies for streaming
pip install python-multipart
```

## Components

The streaming module provides four main components:

1. **`get_streaming_html()`**: Generates HTML markup for the streaming form
2. **`get_streaming_js()`**: Generates JavaScript code to handle streaming responses
3. **`stream_response()`**: Creates a FastAPI StreamingResponse from an async generator
4. **`create_streaming_endpoint()`**: Utility to create a streaming endpoint with minimal code

## Usage

### Basic Implementation

1. Import the streaming utilities:

```python
from framework_hexagonal.utils.streaming import get_streaming_html, get_streaming_js, stream_response
```

2. Create a streaming endpoint:

```python
@app.post("/chat-stream")
async def chat_stream(
    message: str = Form(...),
    text_ai: Any = Depends(get_text_ai),
):
    """Stream chat responses."""
    async def generate():
        async for chunk in text_ai.chat(messages=[{"role": "user", "content": message}]):
            yield chunk
    
    return stream_response(generate())
```

3. Pass the streaming utilities to your template:

```python
@app.get("/", response_class=HTMLResponse)
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

4. Use the utilities in your HTML template:

```html
<!-- Add streaming form with custom ID and label -->
{{ get_streaming_html("streaming", "Enter your message") | safe }}

<!-- Add JavaScript to handle streaming responses -->
{{ get_streaming_js("streaming", "/chat-stream") | safe }}
```

### Advanced Usage with Helper Function

For a more concise implementation, use the `create_streaming_endpoint()` helper:

```python
from framework_hexagonal import create_streaming_endpoint

# Define processor function
async def process_message(message: str, text_ai: Any) -> AsyncGenerator[str, None]:
    async for chunk in text_ai.chat(messages=[{"role": "user", "content": message}]):
        yield chunk

# Create endpoint with one line
create_streaming_endpoint(
    app=app,
    path="/chat-stream",
    processor=process_message,
    dependencies=[Depends(get_text_ai)],
)
```

## Common Issues and Solutions

### WebSocket 403 Errors

You may see log messages like:
```
INFO: ('127.0.0.1', 58799) - "WebSocket /ws/chat" 403
INFO: connection rejected (403 Forbidden)
```

**Solution**: These errors are normal and can be ignored. They occur because:
- Some browser features attempt to establish WebSocket connections
- The framework uses HTTP streaming rather than WebSockets
- No WebSocket endpoint exists at `/ws/chat`

### Missing Dependencies

If you see:
```
Form data requires "python-multipart" to be installed.
```

**Solution**: Install the python-multipart package:
```bash
pip install python-multipart
```

### Import Errors

If you encounter:
```
ImportError: cannot import name 'get_streaming_html' from 'framework_hexagonal.utils.streaming'
```

**Solution**: Make sure your framework version is up to date. The streaming utilities were added in version 0.1.0.

### Address Already in Use

When starting the application:
```
ERROR: [Errno 48] Address already in use
```

**Solution**: Kill existing processes using the port:
```bash
lsof -i :8000 | grep LISTEN  # Find process IDs
kill -9 <PID>                # Kill the processes
```

## Examples

Two example implementations are provided:

1. **Basic Example**: `framework_hexagonal/examples/streaming_example.py`
2. **Demo Application**: `application/main.py`

Run either example with:
```bash
# Run streaming example
python -m framework_hexagonal.examples.streaming_example

# Run demo application
python -m application.main
``` 