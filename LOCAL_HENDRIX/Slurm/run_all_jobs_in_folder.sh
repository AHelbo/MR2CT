#!/bin/bash

# Get the current directory
current_dir=$(pwd)

# Get a list of all .sh files in the current directory
sh_files=$(find "$current_dir" -maxdepth 1 -type f -name "*.sh")

# Loop through each .sh file
for file in $sh_files; do
    # Exclude the script itself
    if [[ $file != "$current_dir/$0" ]]; then
        # Run sbatch for each file
        echo "Submitted $file to sbatch": 
        sbatch "$file"
    fi
done