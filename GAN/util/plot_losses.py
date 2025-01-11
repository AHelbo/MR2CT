import sys
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from collections import defaultdict



def find_log_files(root_folder):
    
    search_pattern = os.path.join(root_folder, f"**/loss_log.txt")

    files = glob.glob(search_pattern, recursive=True)
    
    return files

def plot_log_p2p(file_path, root_folder):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            if (line[0] == "=" or len(line) < 26): 
                continue

            # Splitting each line by spaces
            parts = line.replace(":",",").replace(" ",",").split(",")
            
            # Extracting relevant information
            epoch = int(parts[2])
            G_GAN = float(parts[17])
            G_L1 = float(parts[20])
            D_real = float(parts[23])
            D_fake = float(parts[26])
            val_G_GAN = float(parts[29])
            val_G_L1 = float(parts[32])
            SSIM = float(parts[35])

            # fix for missing line break
            if (parts[38].count("=") > 0):
                PSNR = float(parts[38].split("=")[0])
            else:
                PSNR = float(parts[38])

            # Appending to data
            data.append([epoch, G_GAN, G_L1, D_real, D_fake, val_G_GAN, val_G_L1, SSIM, PSNR])
    
    data = np.array(data)
    epochs = np.unique(data[:,0])[:-1] #We don't want the most recent epoch, as it may be unreliable

    means = []
    for value in epochs:
        mask = data[: , 0] == value
        subset = data[mask]
        mean_G_GAN = np.mean(subset[:, 1])
        mean_G_L1 = np.mean(subset[:, 2])
        mean_D_real = np.mean(subset[:, 3])
        mean_D_fake = np.mean(subset[:, 4])
        mean_val_G_GAN = np.mean(subset[:, 5])
        mean_val_G_L1 = np.mean(subset[:, 6])
        mean_SSIM = np.mean(subset[:, 7])
        mean_PSNR = np.mean(subset[:, 8])
        
        means.append([value, mean_G_GAN, mean_G_L1, mean_D_real, mean_D_fake, mean_val_G_GAN, mean_val_G_L1, mean_SSIM, mean_PSNR])
    
    means = np.array(means)
    
    plt.style.use('default')
    plt.rcParams.update({'font.size': 16})

    plt.xlim(0, 100)

    fig, axs = plt.subplots(1, 4, figsize=(24, 4))

    # for ax in axs:
    #     ax.spines['top'].set_visible(False)  # Hide the top spine for each subplot
    #     ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.5, zorder=3)
    #     ax.set_facecolor('#f0f0f0')

    plot_graph(axs, 0, "G Train", epochs, means[:, 1], line_color = "steelblue", plot_title = "G and D loss")
    plot_graph(axs, 0, "G Val", epochs, means[:, 5], line_color = "goldenrod")
    plot_graph(axs, 0, "D real", epochs, means[:, 3], line_color = "darkseagreen")
    plot_graph(axs, 0, "D fake", epochs, means[:, 4], line_color = "palevioletred")
    
    plot_graph(axs, 1, "Train", epochs, means[:, 2], line_color = "steelblue", plot_title = "L1 loss")
    plot_graph(axs, 1, "Val", epochs, means[:, 6], line_color = "goldenrod")
    
    plot_graph(axs, 2, "Val", epochs, means[:, 7], line_color = "goldenrod", plot_title = "SSIM")
    
    plot_graph(axs, 3, "Val", epochs, means[:, 8], line_color = "goldenrod", plot_title = "PSNR")
    
    # fig.delaxes(axs[1,0])
    # fig.delaxes(axs[1,1])
    # fig.delaxes(axs[1,2])
    # fig.delaxes(axs[1,3])

    plt.tight_layout()

    # Plotting
    # FLYT UDKOMMENTERING WINDOWS/MAC STIER
    # model = file_path.split("\\")[-2]
    model = file_path.split("/")[-2]

    title = f"{model}_plot"

    # fig.suptitle(title)


    plt.tight_layout()
    plt.savefig(f"{root_folder}/{title}.png") 
    plt.close()


def plot_graph(ax, ax_index, plot_label, x_vals, y_vals, line_color = "blue", plot_title = None):
    if (plot_title):
        ax[ax_index].set_title(plot_title)
    ax[ax_index].grid(visible=True)
    ax[ax_index].plot(x_vals, y_vals, label=plot_label, linewidth=1, color=line_color)
    ax[ax_index].set_xlabel("Epoch")
    ax[ax_index].set_ylabel("Loss")
    ax[ax_index].legend()
    ax[ax_index].spines['top'].set_visible(False)  # Hide the top spine for each subplot
    ax[ax_index].spines['right'].set_visible(False)  # Hide the top spine for each subplot
    ax[ax_index].yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.5, zorder=3)
    ax[ax_index].set_facecolor('#f0f0f0')
    ax[ax_index].set_xlim(0, 80)  # Set the limit for the x-axis
    ax[ax_index].xaxis.set_major_locator(MultipleLocator(10))

    if (ax_index == 0):
        ax[ax_index].set_ylim(0, 6)  # Set the limit for the x-axis

    if (ax_index == 1):
        ax[ax_index].set_ylim(0, 0.1)  # Set the limit for the x-axis

    if (ax_index == 2):
        ax[ax_index].set_ylim(0.6, 0.78)  # Set the limit for the x-axis

    if (ax_index == 3):
        ax[ax_index].set_ylim(19, 23)  # Set the limit for the x-axis              


def rolling_avg(a,n): 
    assert n%2==1
    b = a*0.0
    for i in range(len(a)) :
        b[i]=a[max(i-n//2,0):min(i+n//2+1,len(a))].mean()
    return b

import json

def read_losses(dir):

    losses = defaultdict(lambda: defaultdict(list))

    with open(f'{dir}/loss_log.txt', 'r') as file:
        for line in file:
            
            line = line.strip()  # Remove leading/trailing whitespace
            
            if not line.startswith('{'):  # Check if the line starts with '{'
                print(line)
                continue
            
            # Remove trailing comma and parse the line as JSON
            line = line.rstrip(',')
            data = json.loads(line)
            # Process the JSON object (e.g., print it)
            print(data)
            print(data.epoch)
            print(data.SSIM)




def plot_losses(checkpoint_dir):

    losses = read_losses(checkpoint_dir)

    # plot(checkpoint_dir, losses)