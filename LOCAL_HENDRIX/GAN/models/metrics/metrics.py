from skimage.metrics import structural_similarity

from skimage.metrics import peak_signal_noise_ratio

from skimage.metrics import mean_squared_error

from PIL import Image, ImageOps
import numpy as np

def ssim(A,B):
    print(f"{A.shape =}")
    print(f"{B.shape =}")
    return structural_similarity(A,B)

def psnr(A,B):
    return peak_signal_noise_ratio(A,B)

def mse(A,B):
    return mean_squared_error(A,B)

def torch2imarr(tensor):
    array = tensor.detach().numpy().squeeze(0).squeeze(0)
    imarr = ((array - array.min()) / (array.max() - array.min())) * 255
    return imarr

def torch_ssim(A,B):
    A = torch2imarr(A)
    B = torch2imarr(B)

    d_range = max(A.max(),B.max())-min(A.min(),B.min())

    ssim = structural_similarity(A,B,data_range=d_range)

    return ssim

def torch_psnr(A,B):
    A = torch2imarr(A)
    B = torch2imarr(B)

    d_range = max(A.max(),B.max())-min(A.min(),B.min())


    return peak_signal_noise_ratio(A,B,data_range=d_range)


def torch_mse(A,B):
    A = torch2imarr(A)
    B = torch2imarr(B)

    return mean_squared_error(A,B)


if __name__ == "__main__":
    A_path = "A.jpg"  
    B_path = "B.jpg"  
    C_path = "C.jpg"  
    A = np.array(ImageOps.grayscale(Image.open(A_path)))
    B = np.array(ImageOps.grayscale(Image.open(B_path)))
    C = np.array(ImageOps.grayscale(Image.open(C_path)))

    print(f"{ssim(A,A) =}")
    print(f"{ssim(A,B) =}")

    print(f"{psnr(A,A) =}")
    print(f"{psnr(A,B) =}")
    print(f"{psnr(A,C) =}")

    print(f"{mse(A,A) =}")    
    print(f"{mse(A,B) =}")

    