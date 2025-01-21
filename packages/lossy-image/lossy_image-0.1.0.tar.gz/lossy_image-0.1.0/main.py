from lossy_image.algorithm.jpeg2k import Jpeg2000Algorithm
from lossy_image.algorithm.webp import WebPAlgorithm
from lossy_image.compression import Compression
from lossy_image.evaluation import Evaluator
from lossy_image.metric.psnr import PSNR
from lossy_image.metric.size_ratio import SizeRatio
from lossy_image.metric.ssim import SSIM
from lossy_image.metric.fsim import FSIM
from lossy_image.result import CompressionResult

from PIL import Image


def main():
    comp = Compression('data/reference_images/I01.BMP')
    jpeg_comp_results = comp.compress(WebPAlgorithm(quality=10), output_path='data/compressed/I01_compressed.webp')

    # evall = Evaluator(metrics=[PSNR, FSIM])
    # jpeg_comp_metrics = evall.evaluate(jpeg_comp_results)
    #
    # print(jpeg_comp_metrics)
    # res = CompressionResult('abc', 'def', Image.open('data/reference_images/I01.BMP'), Image.open('data/reference_images/I01.BMP'), 'jpeg', {'my_param': 123})
    # evall = Evaluator([SizeRatio, PSNR, SSIM, FSIM])
    # jpeg_comp_metrics = evall.evaluate(res)
    #
    # print(jpeg_comp_metrics)


if __name__ == '__main__':
    main()
