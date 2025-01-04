import os
import zipfile
from config import OUTPUT_DIR, NC
from src.utils import print_hierarchical

def zip_dataset():  
    zip_path = os.path.join(OUTPUT_DIR, f"mri2ct_nc{NC}.zip")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(OUTPUT_DIR):
                rel_path = os.path.relpath(root, OUTPUT_DIR)
                if rel_path in ["train", "val", "test"]:
                    print_hierarchical(f"Zipping {rel_path} directory", 1)
                
                for file in files:
                    if file.split(".")[-1] == "tiff":
                        abs_file_path = os.path.join(root, file)
                        rel_file_path = os.path.relpath(abs_file_path, os.path.join(OUTPUT_DIR, '..'))
                        zipf.write(abs_file_path, rel_file_path)
        print_hierarchical("Zipped succesfully!", 1)
    
    except Exception as e:
        print(f"Error: {e}")
        return
