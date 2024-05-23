#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=10000M
#SBATCH -p gpu --gres=gpu:titanrtx:1
#SBATCH --time=2-12:00:00

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
python train.py --dataroot ./datasets/mr2ct_pix2pix_nc3 --name pix2pix_bal_nc3 --model pix2pix --display_id -1 --load_size 266 --input_nc 3 --output_nc 1 --n_epochs 2500 --norm batch --batch_size 10 --lr 0.00005 --netG unet_256 --D_update_freq 36 --continue_train --epoch_count 273




