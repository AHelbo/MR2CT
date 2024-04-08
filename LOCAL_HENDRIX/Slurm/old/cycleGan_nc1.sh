#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=6000M
# we run on the gpu partition and we allocate 2 titanx gpus
#SBATCH -p gpu --gres=gpu:titanx:1
#We expect that our program should not run longer than 4 hours
#Note that a program will be killed once it exceeds this time!
#SBATCH --time=6-24:00:00

echo "Doing cluster stuff:"

echo $CUDA_VISIBLE_DEVICES

module load pytorch

module load cuda

cd pix2pix_cycleGan

python3 train.py --dataroot ./datasets/mr2ct_cycleGan_nc1 --name mr2ct_cycleGan_nc1 --model cycle_gan --display_id -1 --load_size 266 --input_nc 1 --output_nc 1 --n_epochs 2500 --epoch_count 10 --continue_train