import sys
import os
import shutil

# rens make_data input-mappen
def clean_input_folder(nifti_input_folder):
    print("Removing existing unpacked data")
    dirs = [os.path.join(nifti_input_folder,dir) for dir in os.listdir(nifti_input_folder) if os.path.isdir(os.path.join(nifti_input_folder, dir))]

    for dir in dirs:
        shutil.rmtree(dir)

    print("Unpacking raw data")
    zips = [os.path.join(nifti_input_folder,elm) for elm in os.listdir(nifti_input_folder) if elm.split(".")[-1] == "zip"]

    for z in zips:
        shutil.unpack_archive(z,os.path.join(nifti_input_folder,z.split(".")[0]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: reset_input.py <path to folder containing original nifti files>")
        
    else:

        nifti_input_folder = sys.argv[1]

        clean_input_folder(nifti_input_folder)
