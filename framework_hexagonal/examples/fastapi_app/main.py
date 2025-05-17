"""Example FastAPI application using the framework."""
import os
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import framework_hexagonal as fh
from framework_hexagonal.adapters.outbound.openai_text import OpenAITextAdapter
from framework_hexagonal.adapters.outbound.openai_image import OpenAIImageAdapter
from framework_hexagonal.adapters.outbound.tavily_search import TavilySearchAdapter
from framework_hexagonal.adapters.outbound.httpx_fetcher import HttpxWebFetcherAdapter
from framework_hexagonal.adapters.outbound.playwright_screenshot import PlaywrightScreenshotterAdapter
from framework_hexagonal.adapters.outbound.sqlalchemy_db import SQLAlchemyDBAdapter

# Create FastAPI app
app = FastAPI(
    title="Framework Hexagonal Demo",
    description="Example FastAPI application using the hexagonal framework",
    version="0.1.0",
)


# Pydantic models for API
class ChatMessage(BaseModel):
    """Chat message model."""
    
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request model."""
    
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None


class AnalyzeRequest(BaseModel):
    """Text analysis request model."""
    
    text: str
    prompt: str
    model: Optional[str] = None


class ImageRequest(BaseModel):
    """Image generation request model."""
    
    prompt: str
    size: Optional[str] = "1024x1024"
    quality: Optional[str] = "standard"
    n: Optional[int] = 1


class SearchRequest(BaseModel):
    """Web search request model."""
    
    query: str
    max_results: Optional[int] = 5


class FetchRequest(BaseModel):
    """Web fetch request model."""
    
    url: str
    selector: Optional[str] = None


class ScreenshotRequest(BaseModel):
    """Screenshot request model."""
    
    url: str
    full_page: Optional[bool] = True
    width: Optional[int] = 1280
    height: Optional[int] = 800


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
            connection_url=os.environ.get("DATABASE_URL"),
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


# API routes
@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    text_ai: Any = Depends(get_text_ai),
):
    """Stream chat responses."""
    async def generate():
        """Generate chat response chunks."""
        try:
            messages = [{"role": m.role, "content": m.content} for m in request.messages]
            async for chunk in text_ai.chat(
                messages=messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                yield chunk
        except Exception as e:
            yield f"Error: {str(e)}"
    
    return StreamingResponse(generate(), media_type="text/plain")


@app.post("/api/analyze")
async def analyze(
    request: AnalyzeRequest,
    text_ai: Any = Depends(get_text_ai),
):
    """Analyze text."""
    try:
        result = await text_ai.analyze(
            text=request.text,
            prompt=request.prompt,
            model=request.model,
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-image")
async def generate_image(
    request: ImageRequest,
    image_ai: Any = Depends(get_image_ai),
):
    """Generate an image."""
    try:
        result = await image_ai.generate_image(
            prompt=request.prompt,
            size=request.size,
            quality=request.quality,
            n=request.n,
        )
        return {"urls": result if isinstance(result, list) else [result]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search")
async def search(
    request: SearchRequest,
    web_search: Any = Depends(get_web_search),
):
    """Search the web."""
    try:
        results = await web_search.search(
            query=request.query,
            max_results=request.max_results,
        )
        return {
            "results": [
                {
                    "title": r.title,
                    "url": r.url,
                    "snippet": r.snippet,
                }
                for r in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fetch")
async def fetch(
    request: FetchRequest,
    web_fetcher: Any = Depends(get_web_fetcher),
):
    """Fetch a web page."""
    try:
        if request.selector:
            text = await web_fetcher.get_text(
                url=request.url,
                selector=request.selector,
            )
            return {"url": request.url, "text": text}
        else:
            page = await web_fetcher.fetch(url=request.url)
            return {
                "url": page.url,
                "status_code": page.status_code,
                "html": page.html,
                "headers": page.headers,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/screenshot")
async def screenshot(
    request: ScreenshotRequest,
    screenshotter: Any = Depends(get_screenshotter),
):
    """Take a screenshot of a web page."""
    try:
        image_bytes = await screenshotter.capture(
            url=request.url,
            full_page=request.full_page,
            width=request.width,
            height=request.height,
        )
        
        # Return the image as a response
        return StreamingResponse(
            iter([image_bytes]),
            media_type="image/png"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Framework Hexagonal Demo API",
        "version": fh.__version__,
        "endpoints": [
            "/api/chat",
            "/api/analyze",
            "/api/generate-image",
            "/api/search", 
            "/api/fetch",
            "/api/screenshot",
        ],
    } 