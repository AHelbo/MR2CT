#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=6000M
#SBATCH -p gpu --gres=gpu:titanrtx:1
#SBATCH --time=0-12:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

echo "Training:"

#Out of the scripts folder
cd ..

#Into GAN folder
cd Metrics

source metrics_env/bin/activate

#Run metrics
bash GAN_metrics.sh pix2pix_nc3 val




