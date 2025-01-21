from abc import ABC, abstractmethod

from PIL.Image import Image

class Algorithm(ABC):
    """Abstract base class for image compression algorithms.

    Attributes:
        properties (dict): A dictionary of algorithm-specific properties.
    """

    def __init__(self, **properties):
        """Initializes the algorithm with specified properties.

        Args:
            **properties: Arbitrary keyword arguments representing algorithm-specific properties.
        """
        self.properties = properties

    @property
    @abstractmethod
    def name(self) -> str:
        """Gets the name of the compression algorithm.

        Returns:
            str: The name of the algorithm.
        """
        pass

    @abstractmethod
    def compress(self, image: Image) -> Image:
        """Compresses the given image using the algorithm.

        Args:
            image (Image): The image to be compressed.

        Returns:
            Image: The compressed image.
        """
        pass
