from src.utils import print_hierarchical
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from config import *

def plot_graph(ax, ax_index, loss_name, epochs, y_vals, line_color = "blue", plot_title = None):
    if (plot_title):
        ax[ax_index].set_title(plot_title)
    ax[ax_index].grid(visible=True)
    ax[ax_index].plot(epochs, y_vals, label=loss_name, linewidth=1, color=line_color)
    ax[ax_index].set_xlabel("Epoch")
    ax[ax_index].set_ylabel("Loss")
    ax[ax_index].legend()
    ax[ax_index].spines['top'].set_visible(False) 
    ax[ax_index].spines['right'].set_visible(False) 
    ax[ax_index].yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.5, zorder=3)
    ax[ax_index].set_facecolor('#f0f0f0')
    ax[ax_index].tick_params(axis='x', rotation=90)
    ax[ax_index].xaxis.set_major_locator(MultipleLocator(GAN_STRIDE))

    if (GAN_XLIM):
        ax[ax_index].set_xlim(0, GAN_XLIM)  

    if (ax_index == 0) and (GAN_GD_YLIMS):
        ax[ax_index].set_ylim(GAN_GD_YLIMS)  

    if (ax_index == 1) and (GAN_L1_YLIMS):
        ax[ax_index].set_ylim(GAN_L1_YLIMS)  

    if (ax_index == 2) and (GAN_SSIM_YLIMS):
        ax[ax_index].set_ylim(GAN_SSIM_YLIMS) 

    if (ax_index == 3) and (GAN_PSNR_YLIMS):
        ax[ax_index].set_ylim(GAN_PSNR_YLIMS)  

def plot_gan_dict(data, model):

    _, axs = plt.subplots(1, 4, figsize=(72, 12))
    epochs = [epoch for epoch in data.keys()]

    plot_graph(axs, 0, "G Train", epochs, [data[epoch]["G_GAN"] for epoch in epochs], line_color = "steelblue", plot_title = "G and D loss")
    plot_graph(axs, 0, "G Val", epochs, [data[epoch]["val_G_GAN"] for epoch in epochs], line_color = "goldenrod")
    plot_graph(axs, 0, "D real", epochs, [data[epoch]["D_real"] for epoch in epochs], line_color = "darkseagreen")
    plot_graph(axs, 0, "D fake", epochs, [data[epoch]["D_fake"] for epoch in epochs], line_color = "palevioletred")
    plot_graph(axs, 1, "Train", epochs, [data[epoch]["G_L1"] for epoch in epochs], line_color = "steelblue", plot_title = "L1 loss")
    plot_graph(axs, 1, "Val", epochs, [data[epoch]["val_G_L1"] for epoch in epochs], line_color = "goldenrod")
    plot_graph(axs, 2, "Val", epochs, [data[epoch]["SSIM"] for epoch in epochs], line_color = "goldenrod", plot_title = "SSIM")
    plot_graph(axs, 3, "Val", epochs, [data[epoch]["PSNR"] for epoch in epochs], line_color = "goldenrod", plot_title = "PSNR")
    
    plt.style.use('default')
    plt.rcParams.update({'font.size': 16})
    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/{model}_plot.png") 
    plt.close()

def plot_gan_dicts(datalist):
    for data, model in datalist:
        print_hierarchical(model,1)
        plot_gan_dict(data, model)


def plot_diffusion_dicts(datalist):
    for data, model in datalist:
        try:
            print_hierarchical(model,1)
            plot_diffusion_dict(data, model)        
        except:
            pass

def plot_diffusion_dict(data, model):

    plt.style.use('default')
    fig, axs = plt.subplots(1, 5, figsize=(24, 8))

    epochs = data.keys()

    # OJECTIVE FUNCTION HANDLED INDEPENDENTLY    
    if ("train_mse_loss" in data[1]):
        objective_function = "MSE"
        obj_loss = np.array([data[epoch]["train_mse_loss"] for epoch, _ in data.items()])
    else:
        objective_function = "MAE"
        obj_loss = np.array([data[epoch]["train_mae_loss"] for epoch, _ in data.items()])

    mae = np.array([data[epoch]["val_mae"] for epoch, _ in data.items()])
    mse = np.array([data[epoch]["val_mse"] for epoch, _ in data.items()])
    ssim = np.array([data[epoch]["val_SSIM"] for epoch, _ in data.items()])
    psnr = np.array([data[epoch]["val_PSNR"] for epoch, _ in data.items()])
    val_step_mse = np.array([data[epoch]["val_step_mse"] for epoch, _ in data.items()])

    plot_graph(axs, 0, "Train", epochs, obj_loss, line_color = "blue", plot_title = objective_function)        
    plot_graph(axs, 0, "Val", epochs, val_step_mse, line_color = "orange")

    plot_graph(axs, 1, "Val", epochs, mse, line_color = "red", plot_title = "MSE")    

    plot_graph(axs, 2, "Val", epochs, mae, line_color = "orange", plot_title = "MAE")    

    plot_graph(axs, 3, "Val", epochs, ssim, line_color = "orange", plot_title = "SSIM")   

    plot_graph(axs, 4, "Val", epochs, psnr, line_color = "orange", plot_title = "PSNR")     

    fig.suptitle(model)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/{model.replace('train','diffusion')}.png")
    plt.close()

def plot__diff_graph(ax, ax_index, plot_label, x_vals, y_vals, line_color = "blue", plot_title = None):
    
    if (plot_title):
        ax[0, ax_index].set_title(plot_title)
    ax[ax_index].grid(visible=True)
    ax[ax_index].plot(x_vals, y_vals, label=plot_label, linewidth=0.5, color=line_color)
    ax[ax_index].set_xlabel("Epoch")
    ax[ax_index].set_ylabel("Loss")
    ax[ax_index].legend()