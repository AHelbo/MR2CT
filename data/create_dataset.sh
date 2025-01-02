#!/bin/bash

# Start timer
start=$(date +%s)

# Check if the number of arguments is less than 1 or greater than 2
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    echo "Usage: $0 <model type> [number of input channels, <1,3,5>, default = 1] [run unpack_raw_data, <0,1>, default 0]"
    exit 1
fi

model="$1"
input_channels="${2:-1}"
run_unpack_raw_data="${3:-0}"
echo "Now creating dataset for $model model with $2 channel(s):"
echo "Model: $model"
echo "Input channels: $input_channels"

# check that the specified model is supported
if [[ $model != "pix2pix" && $model != "palette" ]]; then
    echo "Error: Available datasets are: pix2pix, palette"
    exit 1
fi

# check that number of input channels are balanced
if [ "$input_channels" != 1 ] && [ "$((input_channels % 2))" -ne 1 ]; then
    echo "Error: Optional parameter must be odd if provided."
    exit 1
fi

# Get the absolute path of the MAKEDATA directory
MAKEDATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

## unpack raw data
# Check that the input folder exists
if [ ! -d "$MAKEDATA_DIR/Input_data" ]; then
    echo "Input_data folder does not exist."
    exit 1
fi

#If selected, run unpack_raw_data
if [[ $run_unpack_raw_data -eq "1" ]]; then
    python3 unpack_raw_data.py "$MAKEDATA_DIR/Input_data" "$MAKEDATA_DIR/bad_data.txt"
fi


# Create temp folder
TEMP_DIR="$MAKEDATA_DIR/temp"
# rm -r $TEMP_DIR
mkdir $TEMP_DIR

# zip-function
zip_files() {

    local zip_start=$(date +%s)

    # Access the parameters using $1, $2, etc.
    local zip_path="$1"
    local target_path="$2"
    
    echo "Zipping files..."
    zip -r $zip_path $target_path > /dev/null 2>&1
    echo "Done zipping" 

    local zip_end=$(date +%s)
    local execution_time=$((zip_end - zip_start))
    local execution_time_minutes=$((execution_time / 60))

    echo "Finished zipping datasets. Execution Time: $execution_time_minutes minutes"
}


## pix2pix
if [[ $model == "pix2pix" ]]; then

    # concate from raw to temp
    python3 create_pix2pix.py "$MAKEDATA_DIR/Input_data" "$TEMP_DIR" $input_channels

    TARGET_DIR="$MAKEDATA_DIR/pix2pix_nc$input_channels"

    # if mr2ct_pix2pix_nc1 exists, delete it, then create it
    if [ -d "$TARGET_DIR" ]; then
        echo "folder $TARGET_DIR already exists, will delete and create new"
        rm -r "$TARGET_DIR"
    fi
    
    mkdir "$TARGET_DIR"
    mkdir "$TARGET_DIR/train"
    mkdir "$TARGET_DIR/test"
    mkdir "$TARGET_DIR/val"

    # split from temp into mr2ct_pix2pix_nc1 folder
    python3 split_pix2pix.py "$TEMP_DIR"  "$TARGET_DIR" "$MAKEDATA_DIR/data_split.txt"

    # pack files within that folder into a zip
    zip_files "$TARGET_DIR/mr2ct_pix2pix_nc$input_channels.zip" "pix2pix_tiff_nc$input_channels"

fi

## PALETTE
if [[ $model == "palette" ]]; then

    # move data from raw_date to taget folder(s)
    mkdir "$TEMP_DIR/A"
    mkdir "$TEMP_DIR/B"
    python3 create_AB.py "$MAKEDATA_DIR/Input_data" "$TEMP_DIR" $input_channels

    # We must verify that all A's and B's match!
    python3 verify_palette.py "$TEMP_DIR/A" "$TEMP_DIR/B"

    TARGET_DIR="$MAKEDATA_DIR/mr2ct_palette_nc$input_channels"

    # if mr2ct_CUT_nc1 exists, delete it, then create it
    if [ -d "$TARGET_DIR" ]; then
        echo "folder $TARGET_DIR already exists, will delete and create new"
        rm -r "$TARGET_DIR"
    fi
    
    mkdir "$TARGET_DIR"
    mkdir "$TARGET_DIR/train"
    mkdir "$TARGET_DIR/train/A"
    mkdir "$TARGET_DIR/train/B"
    mkdir "$TARGET_DIR/val"
    mkdir "$TARGET_DIR/val/A"
    mkdir "$TARGET_DIR/val/B"
    mkdir "$TARGET_DIR/test"
    mkdir "$TARGET_DIR/test/A"
    mkdir "$TARGET_DIR/test/B"

    python3 split_PALETTE.py "$TEMP_DIR" "$TARGET_DIR" "$MAKEDATA_DIR/data_split.txt"

    # Verify that all the data is balanced
    python3 verify_palette.py "$TARGET_DIR/train/A" "$TARGET_DIR/train/B"
    python3 verify_palette.py "$TARGET_DIR/val/A" "$TARGET_DIR/val/B"
    python3 verify_palette.py "$TARGET_DIR/test/A" "$TARGET_DIR/test/B"

    # pack files within that folder into a zip
    zip_files "$TARGET_DIR/mr2ct_palette_nc$input_channels.zip" "mr2ct_palette_nc$input_channels"

fi

#clean up after yourself, i aint yo momma
rm -r $TEMP_DIR

# End time
end=$(date +%s)
execution_time=$((end - start))
execution_time_minutes=$((execution_time / 60))

echo "Finished creating datasets. Execution Time: $execution_time_minutes minutes"