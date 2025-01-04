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

            print_hierarchical(f"Processing \"{pID}\" ({i+1}/{len(patients)})",2)

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

                    stack = [mr[i-1], mr[i], mr[i+1]]

                    #if the three slices are not adjacent, we can't make a dataset on it:
                    do_continue = False
                    for j in range(1,len(stack)):
                        if (int(stack[j][-7:-4])-int(stack[j-1][-7:-4]) != 1):
                            do_continue = True
                    if (do_continue):
                        continue
                    
                    # we need to also look at a test set padding, therefore we look a bt further around if we can
                    if i >= (2):
                        stack.append(mr[i - 2])
                    if i <= len(mr) - 3:
                        stack.append(mr[i + 2])

                    # iif i is not in test-set but one or more elm in stack is
                    # if (f"{pID}-{slice}" not in test_data) and (len([elm for elm in stack if f"{pID}-{elm[-7:-4]}" in test_data]) > 0):
                    #     continue

                    #now we "know" the a set can be made!
                    mr_images = [cv2.imread(elm, cv2.IMREAD_GRAYSCALE) for elm in [mr[i-1], mr[i], mr[i+1]]]

                    # Stack grayscale images to form RGB image
                    img_mr = np.stack(mr_images, axis=-1)
                    img_ct = cv2.imread(ct[i]) 

                    if (phase):
                        cv2.imwrite(f"{OUTPUT_DIR}/{phase}/A/{pID}-{slice}.png", img_mr)
                        cv2.imwrite(f"{OUTPUT_DIR}/{phase}//B/{pID}-{slice}.png", img_ct)

                    del img_mr
                    del img_ct
                    gc.collect()

            shutil.rmtree(patient)
