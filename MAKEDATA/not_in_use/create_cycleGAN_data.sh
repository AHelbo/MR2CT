#!/bin/bash

echo "Now creating pix2pix dataset:"

# Start time
start=$(date +%s)


# clean

# rm -r "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data/testA"
# rm -r "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data/testB"
# rm -r "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data/trainA"
# rm -r "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data/trainA"

# mkdir "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data/testA"
# mkdir "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data/testB"
# mkdir "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data/trainA"
# mkdir "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data/trainA"

# Body
# python3 convert_nifti2png.py "/Users/andershelbo/Desktop/MAKEDATA/RAW_DATA"

python3 cycleGan_data.py "/Users/andershelbo/Desktop/MAKEDATA/RAW_DATA" "/Users/andershelbo/Desktop/MAKEDATA/cycleGan-data" "train"

# End time
end=$(date +%s)
execution_time=$((end - start))

echo "Finished creating pix2pix dataset. Execution Time: $execution_time seconds"
