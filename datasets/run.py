from time import time
from config import EXCLUDE_BAD_DATA, OUTPUT_DIR, NC
from src.utils import print_hierarchical
from src.reset_data import reset_data
from src.nifti2png import nifti2png
from src.create_folder_structure import create_folder_structure
from src.create_dataset import create_dataset
from src.verify_dataset import verify_dataset
from src.zip_dataset import zip_dataset

def main():
    print(f"Creating {'single' if NC == 1 else 'multi'}-channel MR2CT dataset:")
    print_hierarchical(f"# of cond image channels: {NC}",1)
    print_hierarchical(f"Exclude bad data: {EXCLUDE_BAD_DATA}",1)

    start_time = time()

    print("\nRemoving existing data and unpacking raw data:")
    reset_data()

    print("\nConverting .nii to .tiff:")
    nifti2png()

    print("\nCreate dataset folder structure:")
    create_folder_structure()

    print("\nCreate dataset:")
    create_dataset()

    print("\nVeryfying dataset:")
    verify_dataset()

    print("\nZipping files:")
    zip_dataset()

    print(f"\033[92m\nSuccessfully created {'single' if NC == 1 else 'multi'}-channel MR2CT dataset. Total time elapsed: {(time()-start_time)/60:.2f} minutes\033[0m")
    print(f"\033[92m{OUTPUT_DIR}\033[0m")

if __name__ == "__main__":
    main()