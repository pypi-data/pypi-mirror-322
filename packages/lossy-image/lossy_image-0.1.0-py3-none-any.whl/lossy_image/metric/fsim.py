from lossy_image.metric import Metric

from piq import fsim
from torchvision.transforms.functional import pil_to_tensor


class FSIM(Metric):
    def calculate(self, og_image, comp_image) -> float:
        return fsim(pil_to_tensor(og_image).unsqueeze(0),
                    pil_to_tensor(comp_image).unsqueeze(0),
                    chromatic=True,
                    data_range=255).item()
