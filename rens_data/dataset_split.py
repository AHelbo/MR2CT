import os
import random
import numpy as np
import shutil
import sys
import time

def split(input_folder, target_folder, train = 0.8, val = 0.2):
    
    for folder in [input_folder,target_folder]:
        if not (os.path.isdir(folder)):
            raise Exception(f"{folder} is not a folder")

    data = [elm for elm in os.listdir(input_folder) if elm.split(".")[-1] == "png"]
    
    random.shuffle(data)

    train, val = np.split(data, [int(len(data)*train)])

    for elm in train:
        shutil.copy(os.path.join(input_folder, elm), os.path.join(target_folder, "train", elm))
    for elm in val:
        shutil.copy(os.path.join(input_folder, elm), os.path.join(target_folder, "val", elm))

split("/Users/andershelbo/Desktop/MAKEDATA/pix2pix-data/1")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 dataset_split.py <path1> <path2>")

    else:

        start = time.time()

        print("Splitting data data")

        path1 = sys.argv[1]
        
        path2 = sys.argv[2]

        split(path1, path2)

        end = time.time()

        print(f"split_images has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")