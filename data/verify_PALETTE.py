import os
import random
import numpy as np
import shutil
import sys
import time
from files2txt2files import read_list_from_file
import filecmp


def verify(A_dir, B_dir):
    As = set()
    Bs = set()

    for elm in [elm for elm in os.listdir(A_dir) if elm.split(".")[-1] == "tiff"]:
        As.add(elm)

    for elm in [elm for elm in os.listdir(B_dir) if elm.split(".")[-1] == "tiff"]:
        Bs.add(elm)        

    print(f" {len(As) = }")
    print(f" {len(Bs) = }")
    print(f" {len(As - Bs) = }")

    if (len(As - Bs)) == 0:
        print(" All good")
    else:
        print(" Bad, some items in A are not in B or vice versa!")
        diff = As - Bs
        print(diff)
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 verify_PALETTE.py <pathA> <pathB>")

    else:
        print("Verifying that all A's have matching B's:")
        A = sys.argv[1]

        B = sys.argv[2]

        verify(A, B)