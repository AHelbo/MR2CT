import os
from config import GAN_DIR, DIFF_DIR
from src.utils import print_hierarchical

def get_logs(dir, filename):
    loss_log_files = []

    checkpoints = sorted(
        checkpoint for checkpoint in os.listdir(dir) 
        if os.path.isdir(os.path.join(dir, checkpoint))
    )

    for checkpoint in checkpoints:
        print_hierarchical(checkpoint, 1)
        for file in os.listdir(os.path.join(dir,checkpoint)):
            if file == filename:
                loss_log_files.append(os.path.join(dir,checkpoint,file))

    return loss_log_files

def get_gan_logs():
    return get_logs(GAN_DIR, "loss_log.txt")

def get_diffusion_logs():
    return get_logs(DIFF_DIR, "train.log")    


