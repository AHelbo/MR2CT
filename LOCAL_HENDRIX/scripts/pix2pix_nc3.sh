#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=16000M
#SBATCH -p gpu --gres=gpu:titanrtx:4
#SBATCH --time=6-24:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

module load pytorch

module load cuda

echo "Training:"

cd pix2pix_cycleGan

python3 train.py --dataroot ./datasets/mr2ct_pix2pix_nc3 --name mr2ct_pix2pix_nc3 --model pix2pix --display_id -1 --load_size 266 --input_nc 3 --output_nc 1 --n_epochs 2500 --batch_size 32 --gpu_ids 0,1,2,3