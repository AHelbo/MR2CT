import cv2 
import os
import sys
import time
import shutil
from files2txt2files import read_list_from_file
import numpy as np
import tifffile
from PIL import Image

def concat_tiff_horizontally(tiff_path1, tiff_path2):
    array1 = tifffile.imread(tiff_path1)

    array2 = tifffile.imread(tiff_path2)

    # Concatenate the two arrays horizontally
    # Note: This requires both images to have the same height (number of rows)
    if array1.shape[0] != array2.shape[0]:
        raise ValueError("Images do not have the same height and cannot be concatenated horizontally.")

    concatenated_array = np.concatenate((array1, array2), axis=1)

    return concatenated_array


def hconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    # take maximum height
    h_max = max(img.shape[0] for img in img_list)
    # for img in img_list:
        # print(img.shape)

    # resizing images
    im_list_resize = [cv2.resize(img,
                      (int(img.shape[1] * h_max / img.shape[0]), h_max),
                      interpolation=interpolation)
                      for img in img_list]
    # return final image
    return cv2.hconcat(im_list_resize)


def concat_images(input_folder, output_folder, nc):

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

            if not (len(mr) == len(ct)):
                raise Exception(f"{pID} contains uneven mr and ct folders, they must contain the same number of elements")

            for i in range(len(mr)):
                    
                slice = mr[i][-7:-5] # get the slice-number
                
                if (nc == 1): #single image mode
                    img_h_resize = concat_tiff_horizontally(mr[i], ct[i])
                    tifffile.imwrite(f"{output_folder}/{pID}-{slice}.tiff", img_h_resize)

                else: 
                    #We can't make stack from the first and last image
                    if (i == 0) or (i == len(mr)-1):
                        continue

                    stack = [mr[i-1], mr[i], mr[i+1]]

                    #if the three slices are not adjacent, we can't make a dataset on it:
                    do_continue = False
                    for j in range(1,len(stack)):
                        if (int(stack[j][-8:-5])-int(stack[j-1][-8:-5]) != 1):
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

                    img_h_resize = hconcat_resize([img_mr, img_ct])
                    cv2.imwrite(f"{output_folder}/{pID}-{slice}.tiff", img_h_resize)

            # for i in range(len(mr)): # stacking happens here!!!
            #     slice = mr[i][-7:-4] # get the slice-number
            #     img_mr = cv2.imread(mr[i]) 
            #     img_ct = cv2.imread(ct[i]) 
            #     img_h_resize = hconcat_resize([img_mr, img_ct])
            #     cv2.imwrite(f"{output_folder}/{pID}-{slice}.tiff", img_h_resize)   

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 pix2pix_create.py <path1> <path2> <number of channels>")

    else:

        start = time.time()

        path1 = sys.argv[1]
        path2 = sys.argv[2]
        nc = int(sys.argv[3])


        print("Concating data")

        concat_images(path1, path2, nc)

        end = time.time()

        print(f"concat_images has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")