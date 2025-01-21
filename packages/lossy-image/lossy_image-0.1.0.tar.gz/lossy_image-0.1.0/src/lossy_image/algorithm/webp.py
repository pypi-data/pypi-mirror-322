import io

from lossy_image.algorithm import Algorithm

from PIL import Image


class WebPAlgorithm(Algorithm):

    def __init__(self, **properties):
        super().__init__(**properties)
        self.quality = properties.get('quality', 30)

    @property
    def name(self) -> str:
        return 'WEBP'

    def compress(self, image: Image.Image) -> Image.Image:
        buffer = io.BytesIO()
        image.save(buffer, format=self.name, quality_layers=[self.quality / 100], quality_mode='rates', lossless=False)
        return Image.open(buffer)
