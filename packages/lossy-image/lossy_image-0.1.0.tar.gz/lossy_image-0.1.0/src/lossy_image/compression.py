from lossy_image.algorithm import Algorithm
from lossy_image.result import CompressionResult

from PIL import Image


class Compression:
    """Handles image compression using a specified algorithm."""

    def __init__(self, input_path: str):
        """Initializes the Compression instance with an image file.

        Args:
            input_path (str): The file path to the original image.
        """
        self.raw_image_path = input_path
        self.raw_image = Image.open(input_path)
        self.properties = {}


    def compress(self, algo: Algorithm, output_path: str) -> CompressionResult:
        """Compresses the image using the given algorithm and saves the result.

        Args:
            algo (Algorithm): The compression algorithm to use.
            output_path (str): The file path where the compressed image will be saved.

        Returns:
            CompressionResult: An object containing details of the compression process, including
            input and output paths, original and compressed images, algorithm name, and properties.
        """
        compressed_image = algo.compress(self.raw_image)
        self.properties.update(algo.properties)

        compressed_image.save(output_path)

        return CompressionResult(
            self.raw_image_path,
            output_path,
            self.raw_image,
            compressed_image,
            algo.name,
            self.properties
        )


class BatchCompression:
    ...
