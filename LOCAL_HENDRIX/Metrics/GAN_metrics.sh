#!/bin/bash

##### HOUSEKEEPING ###################################

# Start timer
start=$(date +%s)

# Script dir
script_dir=$(dirname "$(readlink -f "$0")")

# Parant dir
parent_dir=$(dirname "$script_dir")

##### BASH PARAMETERS ###################################

# Check if the number of arguments is less than 1 or greater than 2
if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
    echo "Usage: $0 [model name] [phase <val/test>, default=val] [use gpu <0,1>, default=1]"
    exit 1
fi

# Some parameters have default values, some do not:
model_name="$1" 
phase="val"
gpu="${2:-1}"

# check that valid phase is chosen
if [ "$2" ]; then
    if [ "$2" = "val" ] || [ "$2" = "test" ]; then
        phase="$2"
    else
        echo "Error: Invalid value for phase. Allowed values are 'val' or 'test'."
        exit 1
    fi
fi

##### MORE HOUSEKEEPING ###################################

# Output file
output_file="$parent_dir/Metrics/output_$model_name.txt"

# create directory for the model
metrics_model_dir="$parent_dir/Metrics/$model_name"
mkdir $metrics_model_dir

# input_nc=${model_name##*\_}
# input_nc=${model_name##*"c"}
input_nc="1"

# if look at val
if [ "$phase" = "val" ] ; then
    data_dir="$parent_dir/GAN/datasets/val_mr2ct_pix2pix_nc$input_nc"
    mv "$data_dir/test" "$data_dir/temp"
    mv "$data_dir/val" "$data_dir/test"
    mv "$data_dir/temp" "$data_dir/val"
fi
##### MAIN LOOP ###################################

# Gå til GAN/eksperiements/navn på model og loop over ikke-latest, ie. modeller med et tal der går op i fem i sig.
echo "$parent_dir/GAN/checkpoints/$model_name" 
pth_files=$(find "$parent_dir/GAN/checkpoints/$model_name" -maxdepth 1 -type f -name "*G.pth" ! -name "latest_net_G.pth")

for pth in $pth_files; do

    epoch=${pth##*/}
    epoch=${epoch%_*}
    epoch=${epoch%_*}

    echo "Processing epoch $epoch:"

    cd "$parent_dir/GAN"

    # kald test.py på hver af disse tal og på hver mode, for at genererefake-B
    if [[ $gpu -eq "1" ]]; then
        python3 "$parent_dir/GAN/test.py" --dataroot ./datasets/val_mr2ct_pix2pix_nc$input_nc --name $model_name --model pix2pix --input_nc $input_nc --output_nc 1 --num_test -1 --epoch $epoch #--gpu_ids -1 
    else
        # python3 "$parent_dir/GAN/test.py" --dataroot ./datasets/val_mr2ct_$model_name --name $model_name --model pix2pix --input_nc $input_nc --output_nc 1 --num_test -1 --epoch $epoch --gpu_ids -1 
        python3 "$parent_dir/GAN/test.py" --dataroot ./datasets/val_mr2ct_pix2pix_nc$input_nc --name $model_name --model pix2pix --input_nc $input_nc --output_nc 1 --num_test -1 --epoch $epoch --gpu_ids -1 
    fi

    # move the images we are interested in into temp folders
    real_B_dir="$metrics_model_dir/real_B/"
    mkdir $real_B_dir
    fake_B_dir="$metrics_model_dir/fake_B/"
    mkdir $fake_B_dir
    mv "$parent_dir/GAN/results/$model_name/test_$epoch/images/"*_real_B.png $real_B_dir
    mv "$parent_dir/GAN/results/$model_name/test_$epoch/images/"*_fake_B.png $fake_B_dir

    # Ensure that the two folders contain paired data, ie. for file A_real_B.png must exist a A_fake_B.png
    cd "$parent_dir/Metrics"
    python3 verify_folder_contents.py $real_B_dir $fake_B_dir

    # compare each datapint using element-wise metrics, ssim, psnr etc..
    python3 compare_elementwise.py $real_B_dir $fake_B_dir $epoch $output_file

    #compare SDC
    python3 calculate_SDC.py $real_B_dir $fake_B_dir $epoch $output_file

    # FID på datasætene som helhed, gem til samme txt-fil med samme struktur som foregående
    python3 resize.py $real_B_dir
    python3 resize.py $fake_B_dir
    python3 verify_folder_contents.py $real_B_dir $fake_B_dir

    if [[ $gpu -eq "1" ]]; then
        FID=$(python3 -m pytorch_fid "$real_B_dir" "$fake_B_dir" --device cuda:0)
    else
        FID=$(python3 -m pytorch_fid "$real_B_dir" "$fake_B_dir")
    fi
    FID=${FID#*:}        
    FID=${FID//[[:space:]]/}
    echo "EPOCH $epoch FID $FID" >> $output_file

    # remove temp real and fake dirs
    rm -r $real_B_dir
    rm -r $fake_B_dir

done

# if look at val
if [ "$phase" = "val" ] ; then
    data_dir="$parent_dir/GAN/datasets/val_mr2ct_pix2pix_nc$input_nc"
    mv "$data_dir/test" "$data_dir/temp"
    mv "$data_dir/val" "$data_dir/test"
    mv "$data_dir/temp" "$data_dir/val"
fi

python3 plot_metrics.py $output_file

##### EVEN MORE HOUSEKEEPING ###################################

rm -r $metrics_model_dir

rm $output_file
