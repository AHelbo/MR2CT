#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=6000M
#SBATCH -p gpu --gres=gpu:titanrtx:1
#SBATCH --time=00:10:00

echo "Slurm test"

python3 -m venv test_env

source test_env/bin/activate

pip install scikit-image

python3 test.py