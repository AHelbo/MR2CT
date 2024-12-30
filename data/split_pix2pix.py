import os
import numpy as np
import shutil
import sys
import time
from files2txt2files import read_list_from_file

    
def split(input_folder, target_folder, data_split):

    for folder in [input_folder,target_folder]:
        if not (os.path.isdir(folder)):
            raise Exception(f"{folder} is not a folder")

    all_data = [elm for elm in os.listdir(input_folder) if elm.split(".")[-1] == "tiff"]
    
    split = read_list_from_file(data_split)

    train_pids = [elm.split("=")[0] for elm in split if elm.split("=")[1] == "train"]
    val_pids = [elm.split("=")[0] for elm in split if elm.split("=")[1] == "val"]
    test_pids = [elm.split("=")[0] for elm in split if elm.split("=")[1] == "test"]

    train_set = [elm for elm in all_data if elm.split("-")[0] in train_pids]
    val_set = [elm for elm in all_data if elm.split("-")[0] in val_pids]
    test_set = [elm for elm in all_data if elm.split("-")[0] in test_pids]

    for elm in train_set:
        shutil.copy(os.path.join(input_folder, elm), os.path.join(target_folder, "train", elm))
    for elm in val_set:
        shutil.copy(os.path.join(input_folder, elm), os.path.join(target_folder, "val", elm))
    for elm in test_set:
        shutil.copy(os.path.join(input_folder, elm), os.path.join(target_folder, "test", elm))        

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 dataset_split.py <path1> <path2>")

    else:

        start = time.time()

        print("Splitting pix2pix data")

        path1 = sys.argv[1]
        
        path2 = sys.argv[2]

        data_split = sys.argv[3]

        split(path1, path2, data_split)

        end = time.time()

        print(f"split_images has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")