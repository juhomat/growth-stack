"""OpenAI adapter for ImageAI port."""
from typing import List, Optional, Any, Union
import os
from openai import AsyncOpenAI
from ...core.ports.image_ai import ImageAI


class OpenAIImageAdapter:
    """OpenAI implementation of the ImageAI port."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: str = "dall-e-3",
        default_size: str = "1024x1024",
        timeout: float = 120.0,
    ):
        """
        Initialize the OpenAI image adapter.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            base_url: Optional base URL for the API
            default_model: Default model to use
            default_size: Default image size
            timeout: Timeout for API calls in seconds
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.default_model = default_model
        self.default_size = default_size
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

    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1,
        **kwargs: Any,
    ) -> Union[str, List[str]]:
        """
        Generate images based on a text prompt.

        Args:
            prompt: Text description of the desired image
            size: Image dimensions (e.g., "1024x1024")
            quality: Image quality level
            n: Number of images to generate
            **kwargs: Additional provider-specific parameters

        Returns:
            URL(s) to the generated image(s)
        """
        model = kwargs.pop("model", self.default_model)
        
        # Create the image(s)
        response = await self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
            **kwargs,
        )
        
        # Extract the URLs
        urls = [item.url for item in response.data if item.url]
        
        # Return a single URL or a list depending on n
        return urls[0] if n == 1 and urls else urls

    async def edit_image(
        self,
        image: bytes,
        mask: Optional[bytes] = None,
        prompt: str = "",
        size: str = "1024x1024",
        **kwargs: Any,
    ) -> str:
        """
        Edit an existing image based on a prompt.

        Args:
            image: The source image data
            mask: Optional mask defining areas to edit
            prompt: Instructions for the edit
            size: Output image dimensions
            **kwargs: Additional provider-specific parameters

        Returns:
            URL to the edited image
        """
        # TODO: Implement image editing when available in the AsyncOpenAI client
        # This is a placeholder for future implementation
        raise NotImplementedError(
            "Image editing is not yet implemented in this adapter. "
            "This feature will be available in a future release."
        ) 