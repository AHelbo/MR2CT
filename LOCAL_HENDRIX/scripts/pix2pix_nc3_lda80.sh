#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=16000M
#SBATCH -p gpu --gres=gpu:titanrtx:1
#SBATCH --time=6-24:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

module load pytorch

module load cuda

echo "Training:"

cd pix2pix_cycleGan

python3 train.py --dataroot ./datasets/mr2ct_pix2pix_nc3 --name mr2ct_pix2pix_nc3_lda80 --model pix2pix --display_id -1 --load_size 266 --input_nc 3 --output_nc 1 --n_epochs 2500 --lambda_L1 80