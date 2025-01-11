import os

# Dataset creation parameters
NC = 3
EXCLUDE_BAD_DATA = False
GLOBAL_CT_MIN = -1000
GLOBAL_CT_MAX = 2000

# Directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "raw_data")
OUTPUT_DIR = os.path.join(BASE_DIR, f"mri2ct_nc{NC}")

# Filters
DATA_SPLIT = os.path.join(BASE_DIR, "src", "filters", "data_split.txt")
BAD_DATA = os.path.join(BASE_DIR, "src", "filters", "bad_data.txt")
