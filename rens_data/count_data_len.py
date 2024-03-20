import cv2 
import os

ct_min = 1000000000
ct_max = 0
mr_min = 100000000
mr_max = 0

def count_images(input_folder):

    global ct_min, ct_max, mr_min, mr_max

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

            if (len(mr) > mr_max):
                mr_max = len(mr)
            if (len(mr) < mr_min):
                mr_min = len(mr)

            if (len(ct) > ct_max):
                ct_max = len(mr)
            if (len(ct) < ct_min):
                ct_min = len(mr)

            print(f"{len(ct) = } {len(mr) = } {len(mr) == len(ct)}")
                                           

count_images("/Users/andershelbo/Desktop/MAKEDATA/Pelvis-Data")

print(f"{ct_min = } {ct_max = } {mr_min = } {mr_max = }")