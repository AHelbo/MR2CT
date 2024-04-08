#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=6000M
# we run on the gpu partition and we allocate 2 titanx gpus
#SBATCH -p gpu --gres=gpu:titanrtx:1
#We expect that our program should not run longer than 4 hours
#Note that a program will be killed once it exceeds this time!
#SBATCH --time=24:00:00

echo "Doing cluster stuff:"

echo $CUDA_VISIBLE_DEVICES

module load pytorch

module load cuda

source CUT_nc3_env/bin/activate

pip install packaging

cd CUT

python3 train.py --dataroot ./datasets/mr2ct_CUT_nc3 --name mr2ct_CUT_nc3 --CUT_mode CUT --display_id -1 --load_size 266 --input_nc 3 --output_nc 1
