from src.utils import print_hierarchical
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from config import BASE_DIR, GAN_GD_YLIMS, GAN_L1_YLIMS, GAN_SSIM_YLIMS, GAN_PSNR_YLIMS, GAN_XLIM, GAN_STRIDE, PLOT_DIR

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
