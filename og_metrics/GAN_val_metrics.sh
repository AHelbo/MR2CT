#!/bin/bash
##### BASH PARAMETERS ###################################

# Check if the number of arguments is less than 1 or greater than 2
if [ "$#" -lt 1 ] || [ "$#" -gt 6 ]; then
    echo "Usage: $0 [model name] [phase <test, val>] [start epoch <5,..,5*n>, default=5] [end epoch <5,..,5*n>, default=5] [use gpu <0,1>, default=0] [n_threads <1,..,inf>, default=1]"
    exit 1
fi

# Some parameters have default values, some do not:
model_name="$1" 
start_epoch="$3" 
end_epoch="$4" 
gpu="${5:-1}"
phase="$2"
n_threads="${6:-1}"

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

# define the number of input channels
input_nc=${model_name##*\_}
input_nc=${model_name##*"c"}


##### MAIN LOOP ###################################
# define how we process epochs as a function, that makes it simple to parallelize later
process_epoch(){
    epoch=$1
    if [[ $gpu -eq "1" ]]; then
        gpu_id=$2
    else
        gpu_id=-1
    fi

    echo "Processing epoch $epoch:"

    # If .pth files for this epoch do not exist, return without doing anything
    checkpoints_folder="$parent_dir/GAN/checkpoints/$model_name/"
    if [ ! -f "${checkpoints_folder}/${epoch}_net_D.pth" ] || [ ! -f "${checkpoints_folder}/${epoch}_net_G.pth" ]; then
        echo "Missing D or G for epoch ${epoch}"
        return
    fi


    # Define outputfile for the current epoch
    epoch_output_file="$parent_dir/Metrics/output_${model_name}_epoch${epoch}.txt"
    # Check if the file already exists, exit if it does
    if [[ -f "$epoch_output_file" ]]; then
        echo "File $epoch_output_file already exists. Exiting function."
        return  # Exit the function
    fi    


    echo "Checking if epoch already exists in results folder:"
    results_folder="$parent_dir/GAN/results/$model_name/${phase}_$epoch/"

    cutoff_val=27000
    if [[ $phase == "test" ]]; then
        cutoff_val=14000
    fi
    
    if [[ -d "$results_folder" ]] && (( $(find "$results_folder/images/" -type f | wc -l) > $cutoff_val )); then
        echo "Folder '$results_folder' exists and contains more than $cutoff_val files."
    else
        echo "Folder '$results_folder' does not exist or contains $cutoff_val or fewer files."
        # kald test.py på hver af disse tal og på hver mode, for at generere fake-Bs
        cd "$parent_dir/GAN"
        python3 "$parent_dir/GAN/test.py" --dataroot ./datasets/mr2ct_pix2pix_nc$input_nc --name $model_name --model pix2pix --input_nc $input_nc --output_nc 1 --num_test -1 --epoch $epoch --gpu_ids $gpu_id --phase $phase --load_size 256 --no_flip
    fi

    # copy the images we are interested in into temp folders
    real_B_dir="$metrics_model_dir/real_B$epoch/"
    mkdir $real_B_dir
    fake_B_dir="$metrics_model_dir/fake_B$epoch/"
    mkdir $fake_B_dir

    # cp has a limit (arg list length), so use a loop
    for real_file in "$parent_dir/GAN/results/$model_name/${phase}_${epoch}/images/"*_real_B.png; do
        fake_file="${real_file/_real_B.png/_fake_B.png}"
        cp "$real_file" "$real_B_dir"
        cp "$fake_file" "$fake_B_dir"
    done

    # Ensure that the target/results contains paired data, ie. for file A_real_B.png must exist a A_fake_B.png
    cd "$parent_dir/Metrics"

    python3 ${script_dir}/verify_folder_contents.py $real_B_dir $fake_B_dir

    # compare each datapint using element-wise metrics, ssim, psnr etc..
    python3 ${script_dir}/compare_elementwise.py $real_B_dir $fake_B_dir $epoch $epoch_output_file $gpu

    #compare SIMOS
    python3 ${script_dir}/calculate_SIMOS.py $real_B_dir $fake_B_dir $epoch $epoch_output_file

    # FID på datasætene som helhed, gem til samme txt-fil med samme struktur som foregående
    python3 ${script_dir}/resize.py $real_B_dir
    python3 ${script_dir}/resize.py $fake_B_dir
    python3 ${script_dir}/verify_folder_contents.py $real_B_dir $fake_B_dir

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

    rm -r $results_folder

}


# Loop over the epochs withing the range of $start_epoch and $end_epoch
epochs=$(seq $start_epoch 5 $end_epoch)
for epoch in $epochs; do
    ((i=i%${n_threads})); ((i++==0)) && wait
    process_epoch $epoch $((i-1)) &
done
wait


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
