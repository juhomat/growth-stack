"""
Demo application showing all functionalities of the hexagonal framework.
This application provides a simple web interface to test all adapters.
"""
import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Import the framework
import framework_hexagonal as fh
from framework_hexagonal.adapters.outbound.openai_text import OpenAITextAdapter
from framework_hexagonal.adapters.outbound.openai_image import OpenAIImageAdapter
from framework_hexagonal.adapters.outbound.tavily_search import TavilySearchAdapter
from framework_hexagonal.adapters.outbound.httpx_fetcher import HttpxWebFetcherAdapter
from framework_hexagonal.adapters.outbound.playwright_screenshot import PlaywrightScreenshotterAdapter
from framework_hexagonal.adapters.outbound.sqlalchemy_db import SQLAlchemyDBAdapter
from framework_hexagonal.utils.streaming import get_streaming_html, get_streaming_js

# Create FastAPI app
app = FastAPI(
    title="Framework Hexagonal Demo",
    description="Demo application showing all functionalities of the hexagonal framework",
    version="0.1.0",
)

# Set up templates directory
templates = Jinja2Templates(directory="application/templates")

# Create necessary directories
os.makedirs("application/templates", exist_ok=True)
os.makedirs("application/static", exist_ok=True)
os.makedirs("application/static/screenshots", exist_ok=True)
os.makedirs("application/static/images", exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="application/static"), name="static")

# Chat history to store messages
chat_history = []
search_results = []
fetch_results = []
image_results = []
screenshot_results = []

# Register adapters in the container
@app.on_event("startup")
async def startup_event():
    """Register adapters on startup."""
    # Register OpenAI text adapter
    fh.container.register(
        fh.TextAI,
        OpenAITextAdapter(
            api_key=os.environ.get("OPENAI_API_KEY"),
            default_model="gpt-4o",
        ),
    )
    
    # Register OpenAI image adapter
    fh.container.register(
        fh.ImageAI,
        OpenAIImageAdapter(
            api_key=os.environ.get("OPENAI_API_KEY"),
            default_model="dall-e-3",
        ),
    )
    
    # Register Tavily search adapter
    fh.container.register(
        fh.WebSearch,
        TavilySearchAdapter(
            api_key=os.environ.get("TAVILY_API_KEY"),
        ),
    )
    
    # Register HTTPX web fetcher adapter
    fh.container.register(
        fh.WebFetcher,
        HttpxWebFetcherAdapter(),
    )
    
    # Register Playwright screenshotter adapter
    fh.container.register(
        fh.Screenshotter,
        PlaywrightScreenshotterAdapter(),
    )
    
    # Register SQLAlchemy DB adapter
    fh.container.register(
        fh.DBGateway,
        SQLAlchemyDBAdapter(
            connection_url=os.environ.get("DATABASE_URL", "sqlite:///./test.db"),
        ),
    )

# Dependency to get adapters
def get_text_ai():
    """Get TextAI adapter from container."""
    return fh.container.get(fh.TextAI)

def get_image_ai():
    """Get ImageAI adapter from container."""
    return fh.container.get(fh.ImageAI)

def get_web_search():
    """Get WebSearch adapter from container."""
    return fh.container.get(fh.WebSearch)

def get_web_fetcher():
    """Get WebFetcher adapter from container."""
    return fh.container.get(fh.WebFetcher)

def get_screenshotter():
    """Get Screenshotter adapter from container."""
    return fh.container.get(fh.Screenshotter)

def get_db_gateway():
    """Get DBGateway adapter from container."""
    return fh.container.get(fh.DBGateway)

# Main page route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, error: str = None):
    """Render the main page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "chat_history": chat_history,
            "search_results": search_results,
            "fetch_results": fetch_results,
            "image_results": image_results,
            "screenshot_results": screenshot_results,
            "error": error,
            "get_streaming_html": get_streaming_html,
            "get_streaming_js": get_streaming_js,
        },
    )

# Chat route
@app.post("/chat")
async def chat(
    request: Request,
    message: str = Form(...),
    text_ai: fh.TextAI = Depends(get_text_ai),
):
    """Handle chat requests."""
    # Add user message to history
    chat_history.append({"role": "user", "content": message})
    
    # Generate AI response
    messages = [{"role": m["role"], "content": m["content"]} for m in chat_history]
    
    full_response = ""
    async for chunk in text_ai.chat(messages=messages):
        full_response += chunk
    
    # Add AI response to history
    chat_history.append({"role": "assistant", "content": full_response})
    
    # Redirect back to main page
    return RedirectResponse(url="/", status_code=303)

# Streaming chat route
@app.post("/chat-stream")
async def chat_stream(
    message: str = Form(...),
    text_ai: fh.TextAI = Depends(get_text_ai),
):
    """Stream chat responses."""
    # Add user message to history
    chat_history.append({"role": "user", "content": message})
    
    # Generate AI response
    messages = [{"role": m["role"], "content": m["content"]} for m in chat_history]
    
    async def generate():
        full_response = ""
        async for chunk in text_ai.chat(messages=messages):
            full_response += chunk
            yield chunk
        
        # Add the complete response to history after generation
        chat_history.append({"role": "assistant", "content": full_response})
    
    return fh.stream_response(generate())

# Text analysis route
@app.post("/analyze")
async def analyze(
    request: Request,
    text: str = Form(...),
    prompt: str = Form(...),
    text_ai: fh.TextAI = Depends(get_text_ai),
):
    """Analyze text."""
    result = await text_ai.analyze(text=text, prompt=prompt)
    
    # Add to chat history
    chat_history.append({"role": "user", "content": f"Analyze: {text}\nPrompt: {prompt}"})
    chat_history.append({"role": "assistant", "content": result})
    
    # Redirect back to main page
    return RedirectResponse(url="/", status_code=303)

# Image generation route
@app.post("/generate-image")
async def generate_image(
    request: Request,
    prompt: str = Form(...),
    image_ai: fh.ImageAI = Depends(get_image_ai),
):
    """Generate an image."""
    # Generate image
    image_url = await image_ai.generate_image(prompt=prompt)
    
    # Add to image results
    image_results.append({"prompt": prompt, "url": image_url})
    
    # Redirect back to main page
    return RedirectResponse(url="/", status_code=303)

# Web search route
@app.post("/search")
async def search(
    request: Request,
    query: str = Form(...),
    web_search: fh.WebSearch = Depends(get_web_search),
):
    """Search the web."""
    results = await web_search.search(query=query, max_results=5)
    
    # Convert to dict format for template
    formatted_results = [
        {
            "title": r.title,
            "url": r.url,
            "snippet": r.snippet,
        }
        for r in results
    ]
    
    # Store search results
    search_results.clear()
    search_results.extend(formatted_results)
    
    # Redirect back to main page
    return RedirectResponse(url="/", status_code=303)

# Web fetch route
@app.post("/fetch")
async def fetch(
    request: Request,
    url: str = Form(...),
    selector: str = Form(None),
    web_fetcher: fh.WebFetcher = Depends(get_web_fetcher),
):
    """Fetch web content."""
    # Don't pass the selector to fetch if it's None/empty
    if selector:
        content = await web_fetcher.fetch(url=url, selector=selector)
    else:
        content = await web_fetcher.fetch(url=url)
    
    # Convert to string if content is a tuple
    if isinstance(content, tuple):
        content_str = str(content)
    else:
        content_str = content
    
    # Store fetch result
    fetch_results.clear()
    fetch_results.append({
        "url": url,
        "selector": selector,
        "content": content_str[:1000] + ("..." if len(content_str) > 1000 else "")
    })
    
    # Redirect back to main page
    return RedirectResponse(url="/", status_code=303)

# Screenshot route
@app.post("/screenshot")
async def screenshot(
    request: Request,
    url: str = Form(...),
    screenshotter: fh.Screenshotter = Depends(get_screenshotter),
):
    """Take a screenshot of a webpage."""
    # Generate a unique filename
    filename = f"screenshot_{len(screenshot_results)}.png"
    filepath = f"application/static/screenshots/{filename}"
    
    try:
        # Take screenshot with limited height to prevent errors
        # Use full_page=False for potentially very long pages
        # The viewport height is already set to 800 by default
        screenshot_bytes = await screenshotter.capture(
            url=url, 
            full_page=True,
            # Add error handling for very tall pages
            timeout=30.0
        )
        
        # Save screenshot
        with open(filepath, "wb") as f:
            f.write(screenshot_bytes)
        
        # Add to screenshot results
        screenshot_results.append({
            "url": url,
            "filename": filename,
            "path": f"/static/screenshots/{filename}"
        })
        
    except Exception as e:
        # If full page screenshot fails, try with full_page=False
        try:
            screenshot_bytes = await screenshotter.capture(
                url=url, 
                full_page=False,
                timeout=30.0
            )
            
            # Save screenshot
            with open(filepath, "wb") as f:
                f.write(screenshot_bytes)
            
            # Add to screenshot results with note about viewport-only
            screenshot_results.append({
                "url": url,
                "filename": filename,
                "path": f"/static/screenshots/{filename}",
                "note": "Viewport only (page too large for full screenshot)"
            })
        except Exception as e2:
            # Both attempts failed
            return RedirectResponse(url=f"/?error=Screenshot+failed:+{str(e2)}", status_code=303)
    
    # Redirect back to main page
    return RedirectResponse(url="/", status_code=303)

# Clear history route
@app.post("/clear")
async def clear_history():
    """Clear all history."""
    chat_history.clear()
    search_results.clear()
    fetch_results.clear()
    image_results.clear()
    screenshot_results.clear()
    
    # Redirect back to main page
    return RedirectResponse(url="/", status_code=303)

# Run the application
if __name__ == "__main__":
    uvicorn.run("application.main:app", host="127.0.0.1", port=8000, reload=True) 