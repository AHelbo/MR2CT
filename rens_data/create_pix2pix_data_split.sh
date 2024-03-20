#!/bin/bash

echo "Now creating pix2pix dataset:"

# Start time
start=$(date +%s)

# Body
python3 convert_nifti2png.py "/Users/andershelbo/Desktop/MAKEDATA/RAW_DATA"

python3 concat_images.py "/Users/andershelbo/Desktop/MAKEDATA/Pelvis-Data" "/Users/andershelbo/Desktop/MAKEDATA/pix2pix-data"

# End time
end=$(date +%s)
execution_time=$((end - start))

echo "Finished creating pix2pix dataset. Execution Time: $execution_time seconds"
