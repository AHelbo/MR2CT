#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=6000M
#SBATCH -p gpu --gres=gpu:titanrtx:1
#SBATCH --time=6-24:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

module load pytorch

module load cuda

echo "Training:"

cd ..

cd GAN

python3 train.py --dataroot ./datasets/mr2ct_pix2pix_nc1 --name pix2pix_nc1_noL1 --model pix2pix --display_id -1 --load_size 266 --input_nc 1 --output_nc 1 --n_epochs 2500 --train_schedule "[(1, 0, 100, 1)]"