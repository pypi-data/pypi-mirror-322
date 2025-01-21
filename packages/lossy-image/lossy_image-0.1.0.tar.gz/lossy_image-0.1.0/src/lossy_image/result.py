from abc import ABC
from dataclasses import dataclass, field, asdict

from PIL.Image import Image


@dataclass
class Result(ABC):
    """Abstract base class for storing compression or evaluation results.

    Attributes:
        original_path (str): The file path of the original image.
        compressed_path (str): The file path of the compressed image.
    """
    original_path: str
    compressed_path: str

    def to_json(self) -> dict:
        """Converts the result data to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary containing serializable fields of the result.
        """
        return {
            k: v for k, v in asdict(self).items() if k in self._list_serializable()
        }

    def _list_serializable(self) -> list[str]:
        """Specifies the fields that should be included in the JSON serialization.

        Returns:
            list: A list of field names to be serialized.
        """
        return ['original_path', 'compressed_path']


@dataclass
class CompressionResult(Result):
    """Represents the result of an image compression operation.

    Attributes:
        original_image (Image): The original image object.
        compressed_image (Image): The compressed image object.
        algorithm (str): The name of the compression algorithm used.
        parameters (dict): The parameters used during compression.
    """

    original_image: Image
    compressed_image: Image
    algorithm: str
    parameters: dict = field(default_factory=dict)

    def _list_serializable(self):
        return super()._list_serializable() + ['algorithm', 'parameters']


@dataclass()
class EvaluationResult(Result):
    """Represents the result of an image evaluation process.

    Attributes:
        metrics (dict): A dictionary of evaluation metrics and their values.
    """

    metrics: dict = field(default_factory=dict)

    def _list_serializable(self):
        return super()._list_serializable() + ['metrics']
