#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=10000M
#SBATCH -p gpu --gres=gpu:titanx:4
#SBATCH --time=2-0:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

echo "doing metrics:"

#Out of the scripts folder
cd ..

#Into GAN folder
cd Segment

#Activate env and ensure requirements are met

module load pytorch

module load cuda

source seg_env/bin/activate

echo $VIRTUAL_ENV

#Run seg metrics

data_folder="~/GAN/results/pix2pix_bn10_lr5e-5_f10_nc1/test_700/images"
threshold=0.75
sam="sam.pth"

python3 full_seg.py $data_folder $threshold $sam



