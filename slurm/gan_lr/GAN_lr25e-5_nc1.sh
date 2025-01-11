#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=10000M
#SBATCH -p gpu --gres=gpu:titanrtx:1
#SBATCH --time=48:00:00

echo "PREPPING CLUSTER:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

cd ~/GAN

module load cuda

source gan_env/bin/activate

echo "Activated virtual environment: $VIRTUAL_ENV"
echo "Using Python from: $(which python3)"
echo "Using pip from: $(which pip)"

echo "RUNNING SCRIPT:"

#Run training steps
python3 train.py --name GAN_lr25e-5_nc1 --dataroot ../datasets/mri2ct_nc1 --lambda_L1 100 --batch_size 10 --lr 0.00025