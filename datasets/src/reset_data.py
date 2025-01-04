import os
import shutil
from config import INPUT_DIR, OUTPUT_DIR
from src.utils import print_hierarchical

def reset_data():
    if (os.path.isdir(OUTPUT_DIR)):
        print_hierarchical("Deleting existing dataset:",1)
        print_hierarchical(f"Deleting {OUTPUT_DIR}",2)
        shutil.rmtree(OUTPUT_DIR)

    print_hierarchical("Deleting existing unpacked data:",1)
    dirs = [os.path.join(INPUT_DIR,dir) for dir in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, dir))]
    for dir in dirs:
        print_hierarchical(f"Deleting {dir}",2)
        shutil.rmtree(dir)

    print_hierarchical("Unpacking raw data:",1)
    zips = [os.path.join(INPUT_DIR,elm) for elm in os.listdir(INPUT_DIR) if elm.split(".")[-1] == "zip"]

    for z in zips:
        print_hierarchical(f"Unpacking {z}",2)
        shutil.unpack_archive(z,os.path.join(INPUT_DIR,z.split(".")[0]))
