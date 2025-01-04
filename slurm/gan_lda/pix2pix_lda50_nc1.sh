#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=10000M
#SBATCH -p gpu --gres=gpu:titanrtx:1
#SBATCH --time=1-24:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

echo "Training:"

#Out of the scripts folder
cd ..

#Into GAN folder
cd GAN

#Activate env and ensure requirements are met

module load pytorch

module load cuda

source gan_env/bin/activate

#Run training steps
python3 train.py \
  --name GAN_lda50_nc1 \
  --dataroot ../datasets/mri2ct_nc1 \
  --input_nc 1 \
  --output_nc 1 \
  --lambda_L1 50 \
  --gpu_ids 1

