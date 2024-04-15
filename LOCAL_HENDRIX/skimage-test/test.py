from skimage.metrics import structural_similarity
from PIL import Image, ImageOps
import numpy as np


def image2torch(image):
    pass


def ssim(A,B):
    return structural_similarity(A,B)


def torch_ssim(A,B):
    return ssim(image2torch(A), image2torch(B))


if __name__ == "__main__":
    A_path = "A.jpg"  
    B_path = "B.jpg"  
    A = np.array(ImageOps.grayscale(Image.open(A_path)))
    B = np.array(ImageOps.grayscale(Image.open(B_path)))

    print(A.shape)
    print(structural_similarity(A,B))
    print(structural_similarity(A,A))
    # print(structural_similarity(A,B,channel_axis=2))
    # print(structural_similarity(A,A,channel_axis=2))

    