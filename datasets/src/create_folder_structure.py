import os
from config import OUTPUT_DIR
from src.utils import print_hierarchical

def create_folder_structure():
    splits = ["train", "val", "test"]
    categories = ["A", "B"]

    # Loop through and create folders
    for split in splits:
        for category in categories:
            path = os.path.join(OUTPUT_DIR, split, category)
            os.makedirs(path, exist_ok=True)
            print_hierarchical(f"Created: {path}",1)