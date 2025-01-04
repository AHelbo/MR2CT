import numpy as np
import tifffile
import sys
import os

def get_tiff_stats(file_path):
    with tifffile.TiffFile(file_path) as tif:
        image_data = tif.asarray()

    return {
        'min': np.min(image_data),
        'max': np.max(image_data),
        'mean': np.mean(image_data),
        'std': np.std(image_data),
        'shape': image_data.shape,
        'dtype': image_data.dtype
    }

def compare_tiff_files(file_a, file_b):
    stats_a = get_tiff_stats(file_a)
    stats_b = get_tiff_stats(file_b)
    return all(stats_a[key] == stats_b[key] for key in stats_a)

def print_hierarchical(statement, depth):
    """Print a statement with visual indentation based on depth."""
    prefixes = ["", "├─ ", "│  ├─ ", "│     ├─ "]
    print(f"{prefixes[depth]}{statement}")

def verify_directories(dir_a, dir_b):
    files_in_a = {f for f in os.listdir(dir_a) if f.endswith(".tiff")}
    files_in_b = {f for f in os.listdir(dir_b) if f.endswith(".tiff")}

    all_files_identical = all(
        compare_tiff_files(os.path.join(dir_a, file_a), os.path.join(dir_b, file_b))
        for file_a, file_b in zip(files_in_a, files_in_b)
    )

    print_hierarchical(f"dir_a {len(files_in_a) = }", 2)
    print_hierarchical(f"dir_b {len(files_in_b) = }", 2)
    print_hierarchical(f"Set difference {len(files_in_a - files_in_b)}", 2)
    print_hierarchical(f"Test individual files {all_files_identical = }", 2)

    return files_in_a == files_in_b and all_files_identical

def verify_dataset(base_dir_a, base_dir_b):
    success = True
    for split in ["train", "val", "test"]:
        for data_type in ["A", "B"]:
            print_hierarchical(f"Verifying {split} {data_type} data:", 1)
            dir_a = os.path.join(base_dir_a, split, data_type)
            dir_b = os.path.join(base_dir_b, split, data_type)
            verified = verify_directories(dir_a, dir_b)
            success &= verified

    status = "Verification completed successfully!" if success else "Verification failed, some data is misaligned."
    print_hierarchical(status, 1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python verify_dataset.py <base_dir_a> <base_dir_b>")
        sys.exit(1)
    base_dir_a = sys.argv[1]
    base_dir_b = sys.argv[2]

    print(f"Verifying datasets:")
    verify_dataset(base_dir_a, base_dir_b)

if __name__ == "__main__":
    main()
