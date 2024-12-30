import cv2 
import os
import sys
import time
import numpy as np
from files2txt2files import read_list_from_file
from PIL import Image
from tifffile import imread, imwrite

import gc



def do_work(input_folder, output_folder, nc):

    partitions = [os.path.join(input_folder,dir) for dir in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, dir))]

    for partition in partitions:

        patients = [os.path.join(partition,dir) for dir in os.listdir(partition) if os.path.isdir(os.path.join(partition, dir))]

        for patient in patients:

            pID = patient.split("/")[-1]

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
                
                if (nc == 1):
                    # Load MR and CT images as grayscale
                    # Single-slice mode
                    img_mr = imread(mr[i])
                    img_ct = imread(ct[i])



                    # Save images
                    imwrite(f"{output_folder}/A/{pID}-{slice}.tiff", img_mr)
                    imwrite(f"{output_folder}/B/{pID}-{slice}.tiff", img_ct)

                    del img_mr
                    del img_ct

                    gc.collect()



                    # img_mr = cv2.imread(mr[i], cv2.IMREAD_GRAYSCALE) 
                    # img_ct = cv2.imread(ct[i], cv2.IMREAD_GRAYSCALE) 
                    # cv2.imwrite(f"{output_folder}/A/{pID}-{slice}.png", img_mr)
                    # cv2.imwrite(f"{output_folder}/B/{pID}-{slice}.png", img_ct)

                if (nc == 3):
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


                    cv2.imwrite(f"{output_folder}/A/{pID}-{slice}.png", img_mr)
                    cv2.imwrite(f"{output_folder}/B/{pID}-{slice}.png", img_ct)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 CUT_create.py <path1> <path2> <nc>")

    else:

        start = time.time()

        path1 = sys.argv[1]
        path2 = sys.argv[2]
        nc = int(sys.argv[3])

        print("Populating temp folder with data")
        total = do_work(path1, path2, nc)

        end = time.time()

        print(f"Data has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")