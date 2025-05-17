"""
Growth Stack - Main Application

This is the main entry point for the Growth Stack application.
It sets up the FastAPI application, registers the routes,
and configures the dependencies.
"""

import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path

# Import the framework
import framework_hexagonal as fh
from framework_hexagonal.adapters.outbound.playwright_screenshot import PlaywrightScreenshotterAdapter

# Create FastAPI app
app = FastAPI(
    title="Growth Stack - Marketing & Sales Tools",
    description="A comprehensive collection of digital marketing, sales, and website tools.",
    version="0.1.0",
)

# Setup templates and static files
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Create necessary directories
os.makedirs(str(BASE_DIR / "static" / "screenshots"), exist_ok=True)

# Register adapters in the container
@app.on_event("startup")
async def startup_event():
    """Register adapters on startup."""
    # Register Playwright screenshotter adapter
    fh.container.register(
        fh.Screenshotter,
        PlaywrightScreenshotterAdapter(),
    )

# Dependency to get screenshotter
def get_screenshotter():
    """Get Screenshotter adapter from container."""
    return fh.container.get(fh.Screenshotter)

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )

@app.get("/tools/cro-optimizer", response_class=HTMLResponse)
async def cro_optimizer(request: Request, error: str = None):
    """Render the CRO Optimizer tool page."""
    return templates.TemplateResponse(
        "tools/cro_optimizer.html",
        {
            "request": request,
            "error": error
        },
    )

@app.post("/tools/cro-optimizer/analyze")
async def analyze_website(
    request: Request,
    website_url: str = Form(...),
    screenshotter: fh.Screenshotter = Depends(get_screenshotter)
):
    """Take a screenshot of the website and perform CRO analysis."""
    # Generate a unique filename for the screenshot
    import uuid
    filename = f"screenshot_{uuid.uuid4()}.png"
    filepath = str(BASE_DIR / "static" / "screenshots" / filename)
    screenshot_path = f"/static/screenshots/{filename}"
    
    try:
        # Take a full page screenshot
        screenshot_bytes = await screenshotter.capture(
            url=website_url, 
            full_page=True,
            timeout=30.0
        )
        
        # Save the screenshot
        with open(filepath, "wb") as f:
            f.write(screenshot_bytes)
            
        # Render the results page
        return templates.TemplateResponse(
            "tools/cro_results.html",
            {
                "request": request,
                "website_url": website_url,
                "screenshot_path": screenshot_path,
                "full_page": True
            }
        )
    except Exception as e:
        # If full page screenshot fails, try with viewport only
        try:
            screenshot_bytes = await screenshotter.capture(
                url=website_url, 
                full_page=False,
                timeout=30.0
            )
            
            # Save the screenshot
            with open(filepath, "wb") as f:
                f.write(screenshot_bytes)
                
            # Render the results page with a note about viewport
            return templates.TemplateResponse(
                "tools/cro_results.html",
                {
                    "request": request,
                    "website_url": website_url,
                    "screenshot_path": screenshot_path,
                    "full_page": False,
                    "error_note": "Only viewport captured (page too large for full screenshot)"
                }
            )
        except Exception as e2:
            # Both attempts failed
            return templates.TemplateResponse(
                "tools/cro_optimizer.html",
                {
                    "request": request,
                    "error": f"Screenshot failed: {str(e2)}"
                }
            )

# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "glory.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    ) 