import os
import random
import numpy as np
import shutil
import sys
import time

def split(input_folder, target_folder, train = 0.9, test = 0.1):
    
    for folder in [input_folder,target_folder]:
        if not (os.path.isdir(folder)):
            raise Exception(f"{folder} is not a folder")

    all_data = [elm for elm in os.listdir(input_folder) if elm.split(".")[-1] == "jpeg"]
    print(f"{len(all_data) =}")

    pelvis_data = [elm for elm in os.listdir(input_folder) if elm[1] == "P"]
    random.shuffle(pelvis_data)
    p_train, p_test = np.split(pelvis_data, [int(len(pelvis_data)*train)])

    brain_data = [elm for elm in os.listdir(input_folder) if elm[1] == "B"]
    random.shuffle(brain_data)
    b_train, b_test = np.split(brain_data, [int(len(brain_data)*train)])

    print(f"len test elms: {len(p_test) + len(b_test)}")

    for elm in p_test:
        shutil.copy(os.path.join(input_folder, elm), os.path.join(target_folder, elm))

    for elm in b_test:
        shutil.copy(os.path.join(input_folder, elm), os.path.join(target_folder, elm))        


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 dataset_split.py <path1> <path2>")

    else:

        start = time.time()

        print("Splitting data")

        path1 = sys.argv[1]
        
        path2 = sys.argv[2]

        split(path1, path2)

        end = time.time()

        print(f"split_images has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")