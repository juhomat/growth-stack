"""FastAPI streaming utilities."""
from typing import AsyncGenerator, Callable, Any, Dict, Optional
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import StreamingResponse, HTMLResponse

def get_streaming_js(element_id: str, endpoint: str) -> str:
    """
    Generate JavaScript code for streaming from an endpoint to an HTML element.
    
    Args:
        element_id: ID of the element to update with streaming content
        endpoint: Endpoint URL to stream from
        
    Returns:
        JavaScript code as a string
    """
    return f"""
<script>
document.addEventListener('DOMContentLoaded', function() {{
    const streamForm = document.getElementById('{element_id}-form');
    const streamInput = document.getElementById('{element_id}-input');
    const streamButton = document.getElementById('{element_id}-button');
    const streamResult = document.getElementById('{element_id}-result');
    
    if (!streamForm || !streamInput || !streamButton || !streamResult) {{
        console.error('Streaming elements not found');
        return;
    }}
    
    streamForm.addEventListener('submit', async function(e) {{
        e.preventDefault();
        
        const message = streamInput.value.trim();
        if (!message) return;
        
        // Clear previous response and show container
        streamResult.textContent = '';
        streamResult.style.display = 'block';
        
        // Disable input during streaming
        streamButton.disabled = true;
        streamInput.disabled = true;
        
        try {{
            // Make streaming request
            const response = await fetch('{endpoint}', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded',
                }},
                body: new URLSearchParams({{
                    'message': message
                }})
            }});
            
            // Stream the response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {{
                const {{ done, value }} = await reader.read();
                if (done) break;
                
                const text = decoder.decode(value);
                streamResult.textContent += text;
            }}
        }} catch (error) {{
            console.error('Error:', error);
            streamResult.textContent += '\\nError: Failed to get response.';
        }} finally {{
            // Re-enable input
            streamButton.disabled = false;
            streamInput.disabled = false;
            streamInput.value = '';
            streamInput.focus();
        }}
    }});
}});
</script>
"""


def get_streaming_html(element_id: str, label: str = "Message") -> str:
    """
    Generate HTML for a streaming UI component.
    
    Args:
        element_id: Base ID for the streaming component elements
        label: Label for the input field
        
    Returns:
        HTML code as a string
    """
    return f"""
<form id="{element_id}-form">
    <div>
        <label for="{element_id}-input">{label}:</label>
        <textarea id="{element_id}-input" rows="4" placeholder="Enter your message here..."></textarea>
    </div>
    <button type="submit" id="{element_id}-button">Send</button>
</form>
<div id="{element_id}-result" style="display: none; white-space: pre-wrap; margin-top: 10px; padding: 10px; background-color: #f5f5f5; border-radius: 4px;"></div>
"""


def stream_response(generator: AsyncGenerator[str, None]) -> StreamingResponse:
    """
    Create a streaming response from an async generator.
    
    Args:
        generator: Async generator that yields text chunks
        
    Returns:
        StreamingResponse object
    """
    return StreamingResponse(generator, media_type="text/plain")


def create_streaming_endpoint(
    app: FastAPI,
    path: str,
    processor: Callable[[str], AsyncGenerator[str, None]],
    dependencies: Optional[list] = None,
):
    """
    Create a streaming endpoint for an app.
    
    Args:
        app: FastAPI app
        path: Path for the endpoint
        processor: Function that takes a message and returns an async generator
        dependencies: Optional dependencies for the endpoint
    """
    @app.post(path)
    async def streaming_endpoint(
        message: str = Form(...),
        **kwargs
    ):
        """Stream response from the processor."""
        return stream_response(processor(message, **kwargs)) 