#!/bin/bash

#define source paths:
METRICS="hendrix:~/Metrics/*"

#define target path (Metrics folder):
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#scripts are stored in.....
SCRIPTS="$TARGET_DIR/scripts"

CHECKPOINTS="$TARGET_DIR/Outputs"


# Make temp folder
TEMP="${TARGET_DIR}/TEMP"
mkdir $TEMP

# Get checkpoint images and logs
rsync -zarv --include="output_*.txt" --exclude="*" $METRICS "$TEMP"

# Move files to model folder
cd $TEMP
for file in output_*_epoch*.txt; do
    # Strip off 'output_' prefix
    name="${file#output_}"
    # Strip off '_epoch' .. postfix?
    name="${name%_epoch*}"

    mkdir -p $name
    mv $file $name/ 
done


# plot result
for dir in "$TEMP"/*/; do
    model="${dir%/}"
    model="${model##*/}"
    output_file="$TARGET_DIR/output_${model}_.txt"
    cd $dir
    for i in $(ls output_*_epoch*.txt);do 
        cat $i >> $output_file
        # rm $i
    done
    python3 ${SCRIPTS}/plot_metrics.py $output_file
    # rm $output_file
done

# rm -r $TEMP