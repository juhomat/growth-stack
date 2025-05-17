"""ImageAI port for image generation functionality."""
from typing import List, Optional, Protocol, Any, Union


class ImageAI(Protocol):
    """Interface for AI image generation capabilities."""

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
        ...

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
        ... 