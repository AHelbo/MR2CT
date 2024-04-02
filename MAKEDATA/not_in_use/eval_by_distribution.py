import os
import numpy as np
from PIL import Image

import subprocess


def eval_by_dist(folder, outliers):

    good_count = 0
    bad_count = 0
    cutoff = 60000
    data = [elm for elm in os.listdir(folder) if not elm == ".DS_Store"]

    for elm in data:
        
        img_path = os.path.join(folder, elm)
        png_pil_img = Image.open(img_path)
        image = np.array(png_pil_img)

        width = image.shape[1]
        width_half = width // 2
        
        input_image = image[:, :width_half, :]
        target_image = image[:, width_half:, :]

        blck_input = (input_image <= 0).sum()
        blck_output = (target_image <= 0).sum()

        input_mean = np.mean(input_image)
        target_mean = np.mean(target_image)

        # if (np.abs(input_mean-target_mean) > 45):
        if (np.abs(blck_input-blck_output) > cutoff):
            # print(f"Bad: {elm} abs({blck_input} - {blck_output}) = {np.abs(blck_input-blck_output)}")
            bad_count += 1
            os.rename(os.path.join(folder, elm), os.path.join(outliers, elm))

        else: 
            # print(f"Good: {elm} abs({blck_input} - {blck_output}) = {np.abs(blck_input-blck_output)}")
            good_count += 1

    print(f"{good_count = } {bad_count = } {cutoff = } bad% = {good_count/(bad_count+good_count)} sum = {bad_count+good_count}")





# eval_by_dist("/Users/andershelbo/Desktop/MAKEDATA/dist_test","/Users/andershelbo/Desktop/MAKEDATA/outliers")

eval_by_dist("/Users/andershelbo/Desktop/MAKEDATA/pix2pix-data","/Users/andershelbo/Desktop/MAKEDATA/bad_data_pelvis")

# eval_by_dist("/Users/andershelbo/Desktop/manual","/Users/andershelbo/Desktop/MAKEDATA/pix2pix-data/1")
