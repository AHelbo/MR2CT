#!/bin/bash
# normal cpu stuff: allocate cpus, memory
#SBATCH --ntasks=1 --cpus-per-task=10 --mem=16000M
#SBATCH -p gpu --gres=gpu:titanrtx:1
#SBATCH --time=2-24:00:00

echo "Prepping cluster:"

echo "using gpus:"
echo $CUDA_VISIBLE_DEVICES

module load pytorch

module load pandas

python3 -m venv myenv
source myenv/bin/activate
pip3 install -r ./Palette/requirements.txt

module load cuda

echo "Training:"

cd Palette

python3 run.py -p train -c config/mr2ct_nc1.json