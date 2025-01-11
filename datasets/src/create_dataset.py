import cv2 
import os
import numpy as np
import gc
import shutil
from tifffile import imread, imwrite
from src.utils import print_hierarchical


from config import INPUT_DIR, OUTPUT_DIR, NC, DATA_SPLIT

def get_phase(pID):

    with open(DATA_SPLIT, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            if key == pID:
                return value
    return None

def create_dataset():

    partitions = [os.path.join(INPUT_DIR,dir) for dir in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, dir))]
    for i, partition in enumerate(partitions):

        print_hierarchical(f"Starting work on partition \"{partition}\" ({i+1}/{len(partitions)})",1)

        patients = [os.path.join(partition,dir) for dir in os.listdir(partition) if os.path.isdir(os.path.join(partition, dir))]

        for i, patient in enumerate(patients):
            
            pID = patient.split("/")[-1]

            phase = get_phase(pID)

            if (phase != 'train'):
                continue

            print_hierarchical(f"Creating \"{pID}\" ({i+1}/{len(patients)})",2)

            # check at mapperne existerer
            if not (os.path.isdir(os.path.join(patient, "mr"))):
                continue
            if not (os.path.isdir(os.path.join(patient, "ct"))):
                continue

            mr = [os.path.join(patient,"mr",elm) for elm in os.listdir(os.path.join(patient, "mr")) if not elm == ".DS_Store"]
            mr.sort()

            ct = [os.path.join(patient,"ct",elm) for elm in os.listdir(os.path.join(patient, "ct")) if not elm == ".DS_Store"]
            ct.sort()

            for i in range(len(mr)): ###### nc sker her!!!!

                slice = mr[i][-8:-5] # get the slice-number to ensure that slice is always the same
                
                if (NC == 1):
                    # Load MR and CT images as grayscale
                    img_mr = imread(mr[i])
                    img_ct = imread(ct[i])

                    # Save images
                    if (phase):
                        imwrite(f"{OUTPUT_DIR}/{phase}/A/{pID}-{slice}.tiff", img_mr)
                        imwrite(f"{OUTPUT_DIR}/{phase}/B/{pID}-{slice}.tiff", img_ct)

                    del img_mr
                    del img_ct
                    gc.collect()

                if (NC == 3):
                    if (i == 0) or (i == len(mr)-1):
                        continue

                    mr_images = [imread(img) for img in [mr[i-1], mr[i], mr[i+1]]]

                    img_mr = np.stack(mr_images, axis=-1)
                    
                    img_ct = imread(ct[i]) 

                    if (phase):
                        imwrite(f"{OUTPUT_DIR}/{phase}/A/{pID}-{slice}.tiff", img_mr, photometric='rgb')
                        imwrite(f"{OUTPUT_DIR}/{phase}//B/{pID}-{slice}.tiff", img_ct)

                    del img_mr
                    del img_ct
                    gc.collect()

            shutil.rmtree(patient)
