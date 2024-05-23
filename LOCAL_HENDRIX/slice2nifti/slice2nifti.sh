#!/bin/bash

################ Handle input parameters ################################################################
# Check if the number of arguments is less than 1 or greater than 2
if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
    echo "Usage: $0 [Model name] [Chosen epoch] [Reset Input_data folder <0,1> default=0]"
    exit 1
fi

model_name="$1" # pix2pix_bn10_lr5e-5_f10_nc1
epoch="$2"
reset_input="${3:-0}"

################ Folders ################################################################
# Current dir
script_dir=$(dirname "$(readlink -f "$0")")

# Parent's parent directory
grandparent_dir=$(dirname "$(dirname "${script_dir}")")
input_dir="${grandparent_dir}/MAKEDATA/Input_data"

# Path to dir containing samples
model_output_dir="${grandparent_dir}/LOCAL_HENDRIX/GAN/results/${model_name}/test_${epoch}/images"

mkdir "${model_name}"
outputdir="${script_dir}/${model_name}"

echo "${outputdir}"

if [[ $reset_input -eq "1" ]]; then
    python3 reset_input.py $input_dir
fi

python3 make_nifti.py $input_dir $model_output_dir $outputdir