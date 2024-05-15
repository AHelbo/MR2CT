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
python train.py --dataroot ./datasets/mr2ct_pix2pix_nc1 --name pix2pix_bal_nc1 --model pix2pix --display_id -1 --load_size 266 --input_nc 1 --output_nc 1 --n_epochs 2500 --norm batch --batch_size 10 --lr 0.00005 --D_update_freq 5 --netG unet_256 --train_schedule "[(40,100,100,10),(46,100,100,11),(52,100,100,12),(58,100,100,13),(64,100,100,14),(70,100,100,15),(76,100,100,16),(82,100,100,17),(88,100,100,18),(94,100,100,19),(100,100,100,20),(106,100,100,21),(112,100,100,22),(118,100,100,23),(124,100,100,24),(130,100,100,25),(136,100,100,26),(142,100,100,27),(148,100,100,28),(154,100,100,29),(160,100,100,30),(166,100,100,31),(172,100,100,32),(178,100,100,33),(184,100,100,34),(190,100,100,35),(196,100,100,36)]"




