"""
Growth Stack - Main Application

This is the main entry point for the Growth Stack application.
It sets up the FastAPI application, registers the routes,
and configures the dependencies.
"""

import os
import base64
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from typing import List, Dict, Any

# Import the framework
import framework_hexagonal as fh
from framework_hexagonal.adapters.outbound.playwright_screenshot import PlaywrightScreenshotterAdapter
from framework_hexagonal.adapters.outbound.openai_text import OpenAITextAdapter

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
    
    # Register OpenAI text adapter
    fh.container.register(
        fh.TextAI,
        OpenAITextAdapter(
            api_key=os.environ.get("OPENAI_API_KEY"),
            default_model="gpt-4o",
        ),
    )

# Dependencies to get adapters
def get_screenshotter():
    """Get Screenshotter adapter from container."""
    return fh.container.get(fh.Screenshotter)

def get_text_ai():
    """Get TextAI adapter from container."""
    return fh.container.get(fh.TextAI)

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
    screenshotter: fh.Screenshotter = Depends(get_screenshotter),
    text_ai: fh.TextAI = Depends(get_text_ai)
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
        
        # Construct full URL to the screenshot
        base_url = str(request.base_url).rstrip('/')
        screenshot_url = f"{base_url}{screenshot_path}"
        
        # Define CRO analysis prompt
        cro_prompt = """
        Here is a screenshot of a web page. Please provide a detailed Conversion Rate Optimization (CRO) analysis.
        Focus especially on:

        Call-to-action (CTA) placement and clarity
        Headline effectiveness
        Layout and visual hierarchy
        Use of whitespace and readability
        Trust-building elements (social proof, testimonials, etc.)
        Mobile responsiveness (if possible to evaluate from image)
        Anything else that could improve user conversion or reduce friction

        Suggest concrete, prioritized improvements that would likely increase conversions, and explain why they work.

        Assume the goal of the page is to get users to sign up / request a demo / buy a product (you can specify depending on your page).
        """
        
        # Create messages including the image
        messages = [
            {"role": "system", "content": "You are a CRO expert analyzing a website screenshot."},
            {"role": "user", "content": [
                {"type": "text", "text": cro_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": screenshot_url
                    }
                }
            ]}
        ]
        
        # Get analysis from OpenAI
        analysis = ""
        async for chunk in text_ai.chat(messages=messages):
            analysis += chunk
        
        # Render the results page with the analysis
        return templates.TemplateResponse(
            "tools/cro_results.html",
            {
                "request": request,
                "website_url": website_url,
                "screenshot_path": screenshot_path,
                "full_page": True,
                "analysis": analysis
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
            
            # Construct full URL to the screenshot
            base_url = str(request.base_url).rstrip('/')
            screenshot_url = f"{base_url}{screenshot_path}"
            
            # Define CRO analysis prompt
            cro_prompt = """
            Here is a screenshot of a web page. Please provide a detailed Conversion Rate Optimization (CRO) analysis.
            Focus especially on:

            Call-to-action (CTA) placement and clarity
            Headline effectiveness
            Layout and visual hierarchy
            Use of whitespace and readability
            Trust-building elements (social proof, testimonials, etc.)
            Mobile responsiveness (if possible to evaluate from image)
            Anything else that could improve user conversion or reduce friction

            Suggest concrete, prioritized improvements that would likely increase conversions, and explain why they work.

            Assume the goal of the page is to get users to sign up / request a demo / buy a product (you can specify depending on your page).

            NOTE: This is only a partial screenshot showing the visible viewport.
            """
            
            # Create messages including the image
            messages = [
                {"role": "system", "content": "You are a CRO expert analyzing a website screenshot."},
                {"role": "user", "content": [
                    {"type": "text", "text": cro_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": screenshot_url
                        }
                    }
                ]}
            ]
            
            # Get analysis from OpenAI
            analysis = ""
            async for chunk in text_ai.chat(messages=messages):
                analysis += chunk
            
            # Render the results page with the analysis and a note about viewport
            return templates.TemplateResponse(
                "tools/cro_results.html",
                {
                    "request": request,
                    "website_url": website_url,
                    "screenshot_path": screenshot_path,
                    "full_page": False,
                    "error_note": "Only viewport captured (page too large for full screenshot)",
                    "analysis": analysis
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
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    ) 