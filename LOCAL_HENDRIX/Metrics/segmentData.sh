#!/bin/bash

#arguments for segmentation task
data_folder="$1"
sam="$2"

#start venv depending on OS
python -m pip install --user virtualenv
python -m venv seg_venv

if [ "$3" ]; then
    #mac option not checked...
    if [ "$3"  = "mac" ]; then
        source "seg_venv/bin/activate"
    fi
    if [ "$3" = "windows" ]; then
        "seg_venv/Scripts/activate"
    else
        echo "No OS match (mac or windows), cannot activate venv"
        exit 1
    fi
fi

#install SAM and requirments
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install regex 

#run the full_seg file
python full_seg.py $data_folder $sam

#remove the envoirment once segmentations is complete
rm -r seg_venv
