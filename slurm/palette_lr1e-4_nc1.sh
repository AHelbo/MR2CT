#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=16000M
#SBATCH -p gpu --gres=gpu:titanrtx:8
#SBATCH --time=48:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

echo "Training:"

cd ../diffusion

# Remove or comment out the 'module load pytorch' as it's unnecessary

module load pytorch

module load cuda

# Activate the virtual environment
source pal_env/bin/activate

echo "Activated virtual environment: $VIRTUAL_ENV"

# Check which Python is being used
echo "Using Python from: $(which python3)"
echo "Using pip from: $(which pip)"

# Ensure Pillow is installed in the virtual environment
python3 -m pip show Pillow || python3 -m pip install Pillow

python3 run.py -p train -c config/mr2ct_lr1e-4_nc1.json