import cv2 
import os

ct_min_len = 1000000000
ct_max_len = 0
mr_min_len = 100000000
mr_max_len = 0

ct_min_val = 99999999
ct_max_val = 0
mr_min_val = 99999999
mr_max_val = 0

def count_images(input_folder):

    global ct_min_len, ct_max_len, mr_min_len, mr_max_len

    partitions = [os.path.join(input_folder,dir) for dir in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, dir))]

    for partition in partitions:

        patients = [os.path.join(partition,dir) for dir in os.listdir(partition) if os.path.isdir(os.path.join(partition, dir))]

        for patient in patients:

            # check at mapperne existerer
            if not (os.path.isdir(os.path.join(patient, "mr"))):
                continue
            if not (os.path.isdir(os.path.join(patient, "ct"))):
                continue

            mr = [os.path.join(patient,"mr",elm) for elm in os.listdir(os.path.join(patient, "mr")) if not elm == ".DS_Store"]
            mr.sort()

            ct = [os.path.join(patient,"ct",elm) for elm in os.listdir(os.path.join(patient, "ct")) if not elm == ".DS_Store"]
            ct.sort()

            if (len(mr) > mr_max_len):
                mr_max_len = len(mr)
            if (len(mr) < mr_min_len):
                mr_min_len = len(mr)


                

                                           

count_images("/Users/andershelbo/Desktop/MAKEDATA/Pelvis-Data")

print(f"{ct_min_len = } {ct_max_len = } {mr_min_len = } {mr_max_len = }")