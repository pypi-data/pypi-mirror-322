from lossy_image.metric import Metric

from piq import ssim
from torchvision.transforms.functional import pil_to_tensor


class SSIM(Metric):
    def calculate(self, og_image, comp_image) -> float:
        return ssim(pil_to_tensor(og_image).unsqueeze(0),
                    pil_to_tensor(comp_image).unsqueeze(0),
                    data_range=255).item()
