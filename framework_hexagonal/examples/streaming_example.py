"""Example of using streaming utilities with FastAPI."""
import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Load environment variables
load_dotenv()

# Import framework
import framework_hexagonal as fh
from framework_hexagonal.adapters.outbound.openai_text import OpenAITextAdapter
from framework_hexagonal.utils.streaming import get_streaming_html, get_streaming_js

# Create FastAPI app
app = FastAPI(
    title="Streaming Example",
    description="Example of using streaming utilities with FastAPI",
    version="0.1.0",
)

# Set up templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(templates_dir, exist_ok=True)
templates = Jinja2Templates(directory=templates_dir)

# Register OpenAI text adapter
fh.container.register(
    fh.TextAI,
    OpenAITextAdapter(
        api_key=os.environ.get("OPENAI_API_KEY"),
        default_model="gpt-4o",
    ),
)

# Get adapter from container
def get_text_ai():
    """Get TextAI adapter from container."""
    return fh.container.get(fh.TextAI)

# Create streaming processor function
async def process_chat_stream(message: str, text_ai: fh.TextAI) -> AsyncGenerator[str, None]:
    """Process chat messages and stream the response."""
    messages = [{"role": "user", "content": message}]
    async for chunk in text_ai.chat(messages=messages):
        yield chunk

# Create streaming endpoint using utility
fh.create_streaming_endpoint(
    app=app,
    path="/chat-stream",
    processor=process_chat_stream,
    dependencies=[Depends(get_text_ai)],
)

# Main page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main page with streaming UI."""
    return templates.TemplateResponse(
        "streaming.html",
        {
            "request": request,
            "title": "Streaming Example",
        },
    )

# Create the HTML template file
template_path = os.path.join(templates_dir, "streaming.html")
if not os.path.exists(template_path):
    with open(template_path, "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        #streaming-result {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: #f9f9f9;
        }
    </style>
    """ + get_streaming_js("streaming", "/chat-stream") + """
</head>
<body>
    <h1>{{ title }}</h1>
    <p>This example demonstrates how to use the streaming utilities from the framework.</p>
    
    <h2>Chat Streaming</h2>
    """ + get_streaming_html("streaming", "Enter your message") + """
</body>
</html>""")

# Run the app if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("streaming_example:app", host="127.0.0.1", port=8000, reload=True) 