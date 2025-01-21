import sys

from lossy_image.metric import Metric

from PIL.Image import Image


class SizeRatio(Metric):
    def calculate(self, og_image: Image, comp_image: Image) -> float:
        return sys.getsizeof(og_image.tobytes()) / sys.getsizeof(comp_image.tobytes())
