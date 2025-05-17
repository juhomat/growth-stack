"""OpenAI adapter for TextAI port."""
from typing import AsyncGenerator, Dict, List, Optional, Any
import os
import json
import httpx
from openai import AsyncOpenAI
from ...core.ports.text_ai import TextAI


class OpenAITextAdapter:
    """OpenAI implementation of the TextAI port."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: str = "gpt-4o",
        timeout: float = 60.0,
    ):
        """
        Initialize the OpenAI text adapter.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            base_url: Optional base URL for the API
            default_model: Default model to use
            timeout: Timeout for API calls in seconds
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.default_model = default_model
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Provide as parameter or set OPENAI_API_KEY environment variable."
            )
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=base_url,
            timeout=timeout,
        )

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming chat responses from messages.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            model: Optional model identifier
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Yields:
            Text chunks as they are generated
        """
        model_name = model or self.default_model
        
        # Prepare request parameters
        params = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
            **kwargs,
        }
        
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        
        # Make streaming API call
        stream = await self.client.chat.completions.create(**params)
        
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def analyze(
        self,
        text: str,
        prompt: str,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """
        Analyze text based on a prompt.

        Args:
            text: The text to analyze
            prompt: Instructions for the analysis
            model: Optional model identifier
            **kwargs: Additional provider-specific parameters

        Returns:
            Complete analysis result
        """
        model_name = model or self.default_model
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
        
        # Make non-streaming API call
        response = await self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False,
            **kwargs,
        )
        
        return response.choices[0].message.content or "" 