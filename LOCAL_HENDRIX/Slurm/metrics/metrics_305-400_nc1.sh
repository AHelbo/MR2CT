#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=10000M
#SBATCH -p gpu --gres=gpu:titanx:1
#SBATCH --time=1-0:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

echo "doing metrics:"

#Out of the scripts folder
cd ..

#Into GAN folder
cd Metrics

#Activate env and ensure requirements are met

module load pytorch

module load cuda

source metrics_env/bin/activate

echo $VIRTUAL_ENV

echo "Using Python:"
# which python
# python --version

# python -c "import skimage; print('scikit-image loaded successfully')"

# pip install scikit-image
# pip install matplotlib


#Run metrics

bash GAN_val_metrics.sh pix2pix_bn10_lr5e-5_f10_nc1 305 400 1 1




