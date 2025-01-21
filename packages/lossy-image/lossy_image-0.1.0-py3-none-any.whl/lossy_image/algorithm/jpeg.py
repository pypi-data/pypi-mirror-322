import io

from lossy_image.algorithm import Algorithm

from PIL import Image


class JpegAlgorithm(Algorithm):

    def __init__(self, **properties):
        super().__init__(**properties)
        self.quality = properties.get('quality', 30)
        self.subsampling = properties.get('subsampling', '4:2:0')

    @property
    def name(self) -> str:
        return 'JPEG'

    def compress(self, image: Image.Image) -> Image.Image:
        buffer = io.BytesIO()
        image.save(buffer, format=self.name, quality=self.quality, subsampling=self.subsampling)
        return Image.open(buffer)
