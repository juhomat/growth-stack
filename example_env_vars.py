#!/usr/bin/env python3
"""
Simple example to demonstrate environment variable loading in the framework.
This script checks if the OpenAI API key is being loaded correctly from the .env file.
"""
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_env_vars():
    """Check if the required environment variables are available."""
    openai_key = os.environ.get("OPENAI_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY")
    db_url = os.environ.get("DATABASE_URL")

    print("\nEnvironment Variables Check:")
    print("-" * 40)
    
    # Check OpenAI key
    if openai_key:
        if openai_key == "your_openai_api_key_here":
            print("⚠️  OPENAI_API_KEY: Found but still has default placeholder value")
        else:
            # Only show first few and last few characters for security
            visible_part = openai_key[:4] + "..." + openai_key[-4:] if len(openai_key) > 8 else "***"
            print("✅ OPENAI_API_KEY: Found valid key", f"({visible_part})")
    else:
        print("❌ OPENAI_API_KEY: Not found")
    
    # Check Tavily key
    if tavily_key:
        if tavily_key == "your_tavily_api_key_here":
            print("⚠️  TAVILY_API_KEY: Found but still has default placeholder value")
        else:
            visible_part = tavily_key[:4] + "..." + tavily_key[-4:] if len(tavily_key) > 8 else "***"
            print("✅ TAVILY_API_KEY: Found valid key", f"({visible_part})")
    else:
        print("❌ TAVILY_API_KEY: Not found")
    
    # Check DB URL
    if db_url:
        print("✅ DATABASE_URL:", db_url)
    else:
        print("❌ DATABASE_URL: Not found")
    
    print("-" * 40)
    print("Remember to update the .env file with your actual API keys\n")

async def test_framework_loading():
    """Test if the framework adapters can be initialized."""
    try:
        # Only import here to avoid errors if OpenAI isn't installed
        from framework_hexagonal.adapters.outbound.openai_text import OpenAITextAdapter
        
        try:
            # Try initializing the adapter - this will raise an error if the API key is invalid
            adapter = OpenAITextAdapter()
            print("✅ OpenAITextAdapter: Successfully initialized with environment variables")
        except ValueError as e:
            print(f"❌ OpenAITextAdapter initialization failed: {e}")
    except ImportError:
        print("⚠️  OpenAI package not installed. Install with: pip install -e .[openai]")

if __name__ == "__main__":
    check_env_vars()
    asyncio.run(test_framework_loading()) 