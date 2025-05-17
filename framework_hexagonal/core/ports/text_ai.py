"""TextAI port for chat and analysis functionality."""
from typing import AsyncGenerator, Dict, List, Optional, Protocol, Any


class TextAI(Protocol):
    """Interface for text AI capabilities like chat and analysis."""

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
        ...

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
        ... 