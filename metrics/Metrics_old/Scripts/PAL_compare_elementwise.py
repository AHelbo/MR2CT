import sys
from skimage.metrics import structural_similarity

from skimage.metrics import peak_signal_noise_ratio

from skimage.metrics import mean_squared_error

import os

from PIL import Image

import numpy as np


def ssim(reals, fakes, epoch, outputfile, hendrix):

    acc = 0.0
    count = 0
    for real, fake in zip(reals,fakes):
        try:
            real_image = np.array(Image.open(real))
            fake_image = np.array(Image.open(fake))
            d_range = max(real_image.max(),fake_image.max())-min(real_image.min(),fake_image.min())
            if (hendrix):
                acc += structural_similarity(real_image, fake_image, data_range=d_range, multichannel=True)
            else:
                acc += structural_similarity(real_image, fake_image, data_range=d_range)
            count += 1
        except:
            pass
    mean_ssim = acc / count

    result = f"EPOCH {epoch} SSIM {mean_ssim}\n"

    with open(outputfile, "a") as file:
        file.write(result)
    

def psnr(reals, fakes, epoch, outputfile):
    
    acc = 0.0
    count = 0
    for real, fake in zip(reals,fakes):
        try:
            real_image = np.array(Image.open(real))
            fake_image = np.array(Image.open(fake))
            d_range = max(real_image.max(),fake_image.max())-min(real_image.min(),fake_image.min())
            acc += peak_signal_noise_ratio(real_image, fake_image, data_range=d_range)
            count += 1
        except:
            pass
    mean_psnr = acc / count

    result = f"EPOCH {epoch} PSNR {mean_psnr}\n"

    with open(outputfile, "a") as file:
        file.write(result)


def mse(reals, fakes, epoch, outputfile):
        
    acc = 0.0
    count = 0
    for real, fake in zip(reals,fakes):
        try:
            real_image = np.array(Image.open(real))
            fake_image = np.array(Image.open(fake))
            acc += mean_squared_error(real_image, fake_image)
            count += 1
        except:
            pass
    mean_mse = acc / count

    result = f"EPOCH {epoch} MSE {mean_mse}\n"

    with open(outputfile, "a") as file:
        file.write(result)


def mae(reals, fakes, epoch, outputfile):
        
    acc = 0.0
    count = 0
    for real, fake in zip(reals,fakes):

        try:
            real_image = np.array(Image.open(real))
            fake_image = np.array(Image.open(fake))
            mae_sum = np.sum(np.absolute((real_image.astype("float") - fake_image.astype("float"))))
            mae_pp = mae_sum/ (real_image.shape[0]*real_image.shape[1])
            acc += mae_pp
            count += 1
        except:
            pass        

    mean_mae = acc / count

    result = f"EPOCH {epoch} MAE {mean_mae}\n"

    with open(outputfile, "a") as file:
        file.write(result)


def list_of_elements(path):
    elms = [os.path.join(path,elm) for elm in os.listdir(path) if not elm == ".DS_Store"]
    elms.sort()
    return elms    

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 compare_elementwise.py <pathA> <pathB> <epoch> <path to output file> <hendrix>")

    else:
        print("Comparing real B's and fake B's")
        real_B = sys.argv[1]

        reals = list_of_elements(real_B)

        fake_B = sys.argv[2]

        fakes = list_of_elements(fake_B)

        epoch = sys.argv[3]

        hendrix = sys.argv[5] == "1"

        output_file = sys.argv[4]
        print(" SSIM")
        ssim(reals,fakes,epoch,output_file, hendrix)
        print(" PSNR")
        psnr(reals,fakes,epoch,output_file)
        print(" MSE")
        mse(reals,fakes,epoch,output_file)
        print(" MAE")
        mae(reals,fakes,epoch,output_file)