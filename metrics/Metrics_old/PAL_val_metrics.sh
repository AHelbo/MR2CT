#!/bin/bash
##### BASH PARAMETERS ###################################

# Check if the number of arguments is less than 1 or greater than 2
if [ "$#" -lt 1 ] || [ "$#" -gt 6 ]; then
    echo "Usage: $0 [model name] [Target dir] [epoch] [use gpu <0,1>, default=0]"
    exit 1
fi

# Some parameters have default values, some do not:
model_name="$1" 
TARGET_dir="$2" 
epoch="$3" 
gpu="${4:-1}"

##### HOUSEKEEPING ###################################

# Start timer
start=$(date +%s)

# Parent dir
parent_dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# Script dir
script_dir="${parent_dir}/Metrics/Scripts"

# create directory for the model
metrics_model_dir="$parent_dir/Metrics/$model_name"
mkdir $metrics_model_dir


##### PROCESS ###################################
# define how we process epochs as a function, that makes it simple to parallelize later
process_epoch(){
    epoch=$1
    if [[ $gpu -eq "1" ]]; then
        gpu_id=0
    else
        gpu_id=-1
    fi

    echo "Processing epoch $epoch:"

    # Define outputfile for the current epoch
    epoch_output_file="$parent_dir/Metrics/output_${model_name}_epoch${epoch}.txt"
    # Check if the file already exists, exit if it does
    if [[ -f "$epoch_output_file" ]]; then
        echo "File $epoch_output_file already exists. Exiting function."
        return  # Exit the function
    fi    

    # maybe check that GT and OUT exists

    # copy the images we are interested in into temp folders
    real_B_dir="$metrics_model_dir/real_B$epoch/"
    mkdir $real_B_dir
    fake_B_dir="$metrics_model_dir/fake_B$epoch/"
    mkdir $fake_B_dir

    # cp has a limit (arg list length), so use a loop
    for real_file in "$TARGET_dir/GT_"*".png"; do
        fake_file="${real_file/GT/Out}"
        # Check if both real_file and fake_file exist
        if [[ -f "$real_file" && -f "$fake_file" ]]; then
            cp "$real_file" "$real_B_dir"
            cp "$fake_file" "$fake_B_dir"
        fi
    done

    # Ensure that the target/results contains paired data, ie. for file A_real_B.png must exist a A_fake_B.png
    cd "$parent_dir/Metrics"

    python3 ${script_dir}/PAL_verify_folder_contents.py $real_B_dir $fake_B_dir

    # compare each datapint using element-wise metrics, ssim, psnr etc..
    python3 ${script_dir}/PAL_compare_elementwise.py $real_B_dir $fake_B_dir $epoch $epoch_output_file $gpu

    #compare SIMOS
    python3 ${script_dir}/PAL_calculate_SIMOS.py $real_B_dir $fake_B_dir $epoch $epoch_output_file

    # FID på datasætene som helhed, gem til samme txt-fil med samme struktur som foregående
    python3 ${script_dir}/resize.py $real_B_dir
    python3 ${script_dir}/resize.py $fake_B_dir
    python3 ${script_dir}/PAL_verify_folder_contents.py $real_B_dir $fake_B_dir

    if [[ $gpu -eq "1" ]]; then
        FID=$(python3 -m pytorch_fid "$real_B_dir" "$fake_B_dir" --device cuda:${gpu_id})
    else
        FID=$(python3 -m pytorch_fid "$real_B_dir" "$fake_B_dir")
    fi

    FID=${FID#*:}        
    FID=${FID//[[:space:]]/}
    echo "EPOCH $epoch FID $FID" >> $epoch_output_file

    # remove temp real and fake dirs
    rm -r $real_B_dir
    rm -r $fake_B_dir

}


# Loop over the epochs withing the range of $start_epoch and $end_epoch

process_epoch $epoch

##### PROCESS RESULTS ###################################
# To support running the metrics for each epoch in parallel each epoch has its own output file. 
output_file="$parent_dir/Metrics/output_$model_name.txt"
rm $output_file
for i in $(ls output_${model_name}_epoch*.txt);do 
    cat $i >> $output_file
done

python3 ${script_dir}/plot_metrics.py $output_file


##### TIMER ###################################
end=$(date +%s)
execution_time=$((end - start))
execution_time_minutes=$((execution_time / 60))

echo "Finished evaluating epochs $start_epoch through $end_epoch for ${model}. Execution Time: $execution_time_minutes minutes"
