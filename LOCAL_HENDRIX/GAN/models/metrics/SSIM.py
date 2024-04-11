# import the necessary packages
from skimage.metrics import structural_similarity
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

def _fspecial_gauss(size, sigma):
    """Function to create a Gaussian window."""
    radius = size // 2
    y, x = np.mgrid[-radius:radius+1, -radius:radius+1]
    g = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return g / g.sum()

def _filter2(img, window):
    """Function to compute the mean of image pixels under the window."""
    return np.fft.ifft2(np.fft.fft2(img) * np.fft.fft2(window, img.shape)).real


def SSIM(img1, img2, window_size=11, sigma=1.5, K1=0.01, K2=0.03, L=255):
    if not img1.shape == img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    
    # Convert images to float32
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)
    
    # Define constants
    C1 = (K1 * L) ** 2
    C2 = (K2 * L) ** 2
    
    # Create Gaussian window
    window = _fspecial_gauss(window_size, sigma)
    window = window / np.sum(window)
    
    # Compute mean values
    mu1 = _filter2(img1, window)
    mu2 = _filter2(img2, window)
    
    # Compute squared mean values
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    
    # Compute variance and covariance
    sigma1_sq = _filter2(img1 * img1, window) - mu1_sq
    sigma2_sq = _filter2(img2 * img2, window) - mu2_sq
    sigma12 = _filter2(img1 * img2, window) - mu1_mu2
    
    # Compute SSIM
    numerator = (2 * mu1_mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2)
    ssim_map = numerator / denominator
    
    return np.mean(ssim_map)

# image1 = np.array(Image.open("A.png").convert("L"))  # Convert to grayscale
# image2 = np.array(Image.open("B.png").convert("L"))


# # Compute SSIM
# ssim_np = SSIM(image1, image2)

# ssim_sk = structural_similarity(image1, image2)

# print(f"{ssim_np =}")

# print(f"{ssim_sk =}")