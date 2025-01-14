import os

# GAN Plot settings, a tuple of y limits (0,6)
GAN_STRIDE = 10
GAN_GD_YLIMS = None 
GAN_L1_YLIMS = None 
GAN_SSIM_YLIMS = None 
GAN_PSNR_YLIMS = None 
GAN_XLIM = None
# Directories
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PLOT_DIR = os.path.join(BASE_DIR,"plots")
GAN_DIR = os.path.join(PROJECT_DIR,'GAN','checkpoints')
DIFF_DIR = os.path.join(PROJECT_DIR,'diffusion','checkpoints')

