import os
import random
import numpy as np
import shutil
import sys
import time
from files2txt2files import read_list_from_file

    
def split(input_folder, target_folder, test_data_input, train = 0.8, val = 0.2):
    
    AB = [dir for dir in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, dir))]

    for type in AB:

        print(f"Splitting {type}'s!")

        all_data = [elm for elm in os.listdir(os.path.join(input_folder, type)) if elm.split(".")[-1] == "png"]
        
        test_data_list = read_list_from_file(test_data_input)

        train_val_data = [elm for elm in all_data if not elm.split(".")[0] in test_data_list]

        test_data = [elm for elm in all_data if elm.split(".")[0] in test_data_list]

        random.shuffle(train_val_data)

        train_set, val_set = np.split(train_val_data, [int(len(train_val_data)*train)])

        for elm in train_set:
            shutil.copy(os.path.join(input_folder, type, elm), os.path.join(target_folder, f"train{type}", elm))
        for elm in val_set:
            shutil.copy(os.path.join(input_folder, type, elm), os.path.join(target_folder, f"val{type}", elm))
        for elm in test_data:
            shutil.copy(os.path.join(input_folder, type, elm), os.path.join(target_folder, f"test{type}", elm))   

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 cycleGan_split.py <path1> <path2> <test data file path>")

    else:

        start = time.time()

        print("Splitting data")

        path1 = sys.argv[1]
        
        path2 = sys.argv[2]

        test_data = sys.argv[3]

        split(path1, path2, test_data)

        end = time.time()

        print(f"split_images has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")