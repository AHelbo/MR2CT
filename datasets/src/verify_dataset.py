import os
from config import OUTPUT_DIR
from src.utils import print_hierarchical

def verify_AB(A_dir, B_dir):
    As = set()
    Bs = set()

    for elm in [elm for elm in os.listdir(A_dir) if elm.split(".")[-1] == "tiff"]:
        As.add(elm)

    for elm in [elm for elm in os.listdir(B_dir) if elm.split(".")[-1] == "tiff"]:
        Bs.add(elm)        

    print_hierarchical(f"len(As) = {len(As)}", 2)
    print_hierarchical(f"len(Bs) = {len(Bs)}", 2)
    print_hierarchical(f"len(As - Bs) = {len(As - Bs)}", 2)

    return As == Bs

def verify_dataset():
    success = True
    for split in ["train", "val", "test"]:
        print_hierarchical(f"Verifying {split} data:", 1)
        A_dir = os.path.join(OUTPUT_DIR, split, "A")
        B_dir = os.path.join(OUTPUT_DIR, split, "B")
        success = success and verify_AB(A_dir, B_dir)

    if success:
        print_hierarchical("Verification completed successfully!", 1)
    else:
        print_hierarchical("Verification failed, some data is misaligned.", 1)

def main():
    verify_dataset()

if __name__ == "__main__":
    main()
