import cv2 
import os
import sys
import time
import shutil

def hconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    # take maximum height
    h_max = max(img.shape[0] for img in img_list)

    # resizing images
    im_list_resize = [cv2.resize(img,
                      (int(img.shape[1] * h_max / img.shape[0]), h_max),
                      interpolation=interpolation)
                      for img in img_list]
    # return final image
    return cv2.hconcat(im_list_resize)

def concat_images(input_folder, output_folder):

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

            min_len = min(len(mr),len(ct))      

            for i in range(min_len):
                img_mr = cv2.imread(mr[i]) 
                img_ct = cv2.imread(ct[i]) 
                img_h_resize = hconcat_resize([img_mr, img_ct])
                cv2.imwrite(f"{output_folder}/{pID}-{i:03}.jpeg", img_h_resize)


def clean_folder(folder):
    pics = [os.path.join(folder,elm) for elm in os.listdir(folder) if elm.split(".")[-1] == "jpeg"]

    for p in pics:
        os.remove(p)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 concat_images.py <path1> <path2>")

    else:

        start = time.time()

        path1 = sys.argv[1]
        path2 = sys.argv[2]

        print("Cleaning folders")
        clean_folder(path2)

        print("Concating data")
        concat_images(path1, path2)

        end = time.time()

        print(f"concat_images has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")