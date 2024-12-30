#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=16000M
#SBATCH -p gpu --gres=gpu:titanrtx:4
#SBATCH --time=48:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

echo "Training:"

cd ..

cd diffusion

module load pytorch

module load cuda

source diffusion_env/bin/activate

python3 run.py -p train -c config/mr2ct_lr4e-4_nc1.json