import os
import random
import numpy as np
import shutil
import sys
import time
from files2txt2files import read_list_from_file

    
def split(input_folder, target_folder, data_split):
    
    AB = [dir for dir in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, dir))]

    split = read_list_from_file(data_split)

    for img_type in AB:

        print(f"Splitting {img_type}'s!")

        all_data = [elm for elm in os.listdir(os.path.join(input_folder, img_type)) if elm.split(".")[-1] == "png"]

        train_pids = [elm.split("=")[0] for elm in split if elm.split("=")[1] == "train"]
        val_pids = [elm.split("=")[0] for elm in split if elm.split("=")[1] == "val"] 
        test_pids = [elm.split("=")[0] for elm in split if elm.split("=")[1] == "test"]

        train_set = [elm for elm in all_data if elm.split("-")[0] in train_pids]
        val_set = [elm for elm in all_data if elm.split("-")[0] in val_pids] #
        test_set = [elm for elm in all_data if elm.split("-")[0] in test_pids]

        for elm in train_set:
            shutil.copy(os.path.join(input_folder, img_type, elm), os.path.join(target_folder, "train", f"{img_type}", elm))
        for elm in val_set:
            shutil.copy(os.path.join(input_folder, img_type, elm), os.path.join(target_folder, "val", f"{img_type}", elm))
        for elm in test_set:
            shutil.copy(os.path.join(input_folder, img_type, elm), os.path.join(target_folder, "test", f"{img_type}", elm))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 palette_split.py <path1> <path2> <path to data_split>")

    else:

        start = time.time()

        print("Splitting data data")

        path1 = sys.argv[1]
        
        path2 = sys.argv[2]

        test_data = sys.argv[3]

        split(path1, path2, test_data)

        end = time.time()

        print(f"split_images has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")