import sys
import os
import glob
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def find_outdated_files(root_folder):
    
    outdated_file_names = ["**/loss_log.txt", "**/index.html", "**/latest*"]
    outdated_files = []

    for name in outdated_file_names:
        path = os.path.join(root_folder, name)
        outdated_files += glob.glob(path, recursive=True)

    return outdated_files


def delete_outdated_files(files):
    
    for elm in files:
        print(f"Deleting ..{elm[41:]}:")
        subprocess.run(f"rm {elm}", shell=True)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: _____")

    else:

        root_folder = sys.argv[1]

        outdated_files = find_outdated_files(root_folder)

        delete_outdated_files(outdated_files)
      
