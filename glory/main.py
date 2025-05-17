"""
Growth Stack - Main Application

This is the main entry point for the Growth Stack application.
It sets up the FastAPI application, registers the routes,
and configures the dependencies.
"""

import os
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path

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
async def cro_optimizer(request: Request):
    """Render the CRO Optimizer tool page."""
    return templates.TemplateResponse(
        "tools/cro_optimizer.html",
        {
            "request": request,
        },
    )

@app.post("/tools/cro-optimizer/analyze")
async def analyze_website(
    request: Request,
    website_url: str = Form(...)
):
    """Handle CRO Optimizer form submission.
    
    Currently, this is a placeholder for future functionality.
    In the future, this will process the website URL and perform analysis.
    """
    # Placeholder for future functionality
    # For now, just redirect back to the tool page
    return RedirectResponse(url="/tools/cro-optimizer", status_code=303)

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