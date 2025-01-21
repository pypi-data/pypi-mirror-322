from abc import ABC, abstractmethod

from PIL.Image import Image

class Metric(ABC):
    """Abstract base class for image quality assessment metrics."""

    @abstractmethod
    def calculate(self, og_image: Image, comp_image: Image) -> float:
        """Calculates the metric value between the original and compressed images.

        Args:
            og_image (Image): The original image before compression.
            comp_image (Image): The compressed image after processing.

        Returns:
            float: The calculated metric value representing the quality of the compressed image.
        """
        pass
