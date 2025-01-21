
from PIL import Image

from lossy_image.metric import Metric
from lossy_image.result import CompressionResult, EvaluationResult


class Evaluator:
    """Evaluates the quality of compressed images using specified metrics."""

    def __init__(self, metrics: list[Metric]):
        """Initializes the Evaluator with a list of evaluation metrics.

        Args:
            metrics (list[Metric]): A list of metric classes to be used for evaluation.
        """
        self.metrics = metrics
        self.result = None

    def evaluate(self, comp_result: CompressionResult = None, og_path: str = None, comp_path: str = None) -> EvaluationResult:
        """Evaluates the quality of a compressed image based on the provided inputs.

        Args:
            comp_result (CompressionResult, optional): An instance containing compression results.
            og_path (str, optional): Path to the original image.
            comp_path (str, optional): Path to the compressed image.

        Returns:
            EvaluationResult: An object containing evaluation metrics.

        Raises:
            ValueError: If neither `comp_result` nor `og_path` and `comp_path` are provided.
        """
        if comp_result is not None:
            self.result = EvaluationResult(
                comp_result.original_path,
                comp_result.compressed_path
            )
            return self._eval_comp_results(comp_result)
        elif og_path is not None and comp_path is not None:
            self.result = EvaluationResult(
                og_path,
                comp_path
            )
            return self._eval_images(og_path, comp_path)
        else:
            raise ValueError("Either 'comp_result' or both 'og_path' and 'comp_path' must be provided.")


    def _eval_comp_results(self, comp_results: CompressionResult) -> EvaluationResult:
        """Evaluates the compressed results using the original and compressed images from CompressionResult

        Args:
            comp_results (CompressionResult): The result of the compression process.

        Returns:
            EvaluationResult: An object containing computed evaluation metrics.
        """
        return self._calculate_metrics(comp_results.original_image, comp_results.compressed_image)

    def _eval_images(self, og_path: str, comp_path: str) -> EvaluationResult:
        """Loads images from file paths and evaluates their quality.

        Args:
            og_path (str): Path to the original image.
            comp_path (str): Path to the compressed image.

        Returns:
            EvaluationResult: An object containing computed evaluation metrics.
        """
        return self._calculate_metrics(Image.open(og_path), Image.open(comp_path))

    def _calculate_metrics(self, og_image: Image.Image, comp_image: Image.Image) -> EvaluationResult:
        """Calculates evaluation metrics for the given images.

        Args:
            og_image (Image.Image): The original image.
            comp_image (Image.Image): The compressed image.

        Returns:
            EvaluationResult: An object containing computed evaluation metrics.
        """
        for metric_class in self.metrics:
            metric = metric_class()
            self.result.metrics[metric.__class__.__name__.lower()] = metric.calculate(og_image, comp_image)
        return self.result
