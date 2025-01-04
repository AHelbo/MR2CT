# MR2CT Dataset Creation Pipeline

## Overview

This tool automates the process of creating a MR2CT dataset from `.nii` files. It handles everything from resetting data, converting file formats, creating the necessary folder structures, and verifying the dataset, to zipping the final output. The tool can be configured to handle single or multi-channel images and optionally exclude bad data.

## Features

- **Configurable Channel Support**: Supports single or multi-channel MR2CT dataset creation based on the `NC` configuration.
- **Bad Data Handling**: Optionally exclude bad data by setting `EXCLUDE_BAD_DATA` in the configuration.
- **Automated Workflow**: Handles data resetting, conversion, folder structure creation, dataset creation, verification, and zipping in a seamless pipeline.
- **Logging**: Provides hierarchical logging to trace each step of the process.

## Key Functions

This script automates the process of creating a **MR2CT** dataset by processing MRI and CT images, organizing them into the appropriate folder structure, and verifying the dataset's integrity. The pipeline performs a series of steps to process the data, including:
1. Removes any existing dataset files and unpacks raw data.
2. Converts the raw NIfTI files into image files.
3. Creates the necessary folder structure for the dataset.
4. Creates the dataset by organizing image slices.
5. Verifies that the dataset is consistent.
6. Zips the dataset for easy distribution.

## Modules and Functions

### `reset_data()`
- Deletes any existing dataset in the `OUTPUT_DIR` and unpacks the raw data from zip files located in `INPUT_DIR`.

### `nifti2png()`
- Converts NIfTI `.nii.gz` files into TIFF images, saving them in the proper folder structure. The function handles various pre-processing steps, such as scaling and normalizing image values.

### `create_folder_structure()`
- Creates the necessary folder structure under the `OUTPUT_DIR` for splits (`train`, `val`, `test`) and categories (`A`, `B`).

### `create_dataset()`
- Organizes the processed images into their respective folders, following the desired data structure for training and validation splits.

### `verify_dataset()`
- Verifies that the images in the `A` and `B` categories for each split are aligned, ensuring that the dataset is consistent and properly organized.

### `zip_dataset()`
- Zips the entire dataset directory (`train`, `val`, `test`) into a compressed `.zip` file for storage or transfer.

## Configuration

### `NC`
- Defines the number of condition image channels used in the dataset. This is set to `1` by default, but you can change it to process multi-channel data.

### `EXCLUDE_BAD_DATA`
- A flag that determines whether to exclude bad data (e.g., corrupted or unusable images) from processing. This is set to `False` by default.

### `GLOBAL_CT_MIN` and `GLOBAL_CT_MAX`
- Set the global intensity range for CT images. These values are used for intensity normalization and clipping during processing.

### Directories:
- **`BASE_DIR`**: The base directory where the script is located.
- **`INPUT_DIR`**: Directory containing the raw input data (e.g., NIfTI files).
- **`OUTPUT_DIR`**: Directory where the processed dataset will be stored.
  
### Filter Files:
- **`DATA_SPLIT`**: A file that contains the data split configuration.
- **`BAD_DATA`**: A file listing patient scans that should be excluded due to quality issues.

## Execution

To run the dataset creation pipeline, execute the script from the command line:

```bash
python run.py
