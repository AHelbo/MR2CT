#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=16000M
#SBATCH -p gpu --gres=gpu:titanrtx:4
#SBATCH --time=48:00:00

echo "PREPPING CLUSTER:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

cd ~/diffusion

module load cuda

source diffusion_env/bin/activate

echo "Activated virtual environment: $VIRTUAL_ENV"
echo "Using Python from: $(which python3)"
echo "Using pip from: $(which pip)"

echo "RUNNING SCRIPT:"
python3 run.py -p train -c config/lr/mri2ct_lr1e-4_nc1.json