import sys
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def find_log_files(root_folder):
    
    search_pattern = os.path.join(root_folder, f"**/loss_log.txt")

    files = glob.glob(search_pattern, recursive=True)
    
    return files


# def plot_log_cycleGan(file_path, root_folder):
#     data = []

#     with open(file_path, "r") as file:
#         for line in file:
#             if (line[0] == "="):
#                 continue

#             # Splitting each line by spaces
#             parts = line.replace(":",",").replace(" ",",").split(",")
#             # for i, elm in enumerate(parts):
#             #     print(f"{i} {elm}")
#             # Extracting relevant information
#             epoch = int(parts[2])
#             D_A = float(parts[17])
#             G_A = float(parts[20])
#             cycle_A = float(parts[23])
#             idt_A = float(parts[26])
#             D_B = float(parts[29])
#             G_B = float(parts[32])
#             cycle_B = float(parts[35])
#             idt_B = float(parts[38])


#             # Appending to data
#             data.append([epoch, D_A, G_A, cycle_A, idt_A, D_B, G_B, cycle_B, idt_B])
#     data = np.array(data)

#     epochs = np.unique(data[:,0])

#     means = []
#     for value in epochs:
#         mask = data[: , 0] == value
#         subset = data[mask]
#         D_A = np.mean(subset[:, 1])
#         G_A = np.mean(subset[:, 2])
#         cycle_A = np.mean(subset[:, 3])
#         idt_A = np.mean(subset[:, 4])
#         D_B = np.mean(subset[:, 5])
#         G_B = np.mean(subset[:, 6])
#         cycle_B = np.mean(subset[:, 7])
#         idt_B = np.mean(subset[:, 8])
#         means.append([value, D_A, G_A, cycle_A, idt_A, D_B, G_B, cycle_B, idt_B])
#     means = np.array(means)

#     data_dict = {}
#     data_dict["D_A"] = np.column_stack((epochs, means[:, 1]))
#     data_dict["G_A"] = np.column_stack((epochs, means[:, 2]))
#     data_dict["cycle_A"] = np.column_stack((epochs, means[:, 3]))
#     data_dict["idt_A"] = np.column_stack((epochs, means[:, 4]))
#     data_dict["D_B"] = np.column_stack((epochs, means[:, 5]))
#     data_dict["G_B"] = np.column_stack((epochs, means[:, 6]))
#     data_dict["cycle_B"] = np.column_stack((epochs, means[:, 7]))
#     data_dict["idt_B"] = np.column_stack((epochs, means[:, 8]))


#     plt.style.use('seaborn-v0_8')
#     fig, axs = plt.subplots(2, 8, figsize=(24, 8))

#     plot_graph(axs, 0, "D_A", "Train", epochs, means[:, 1])
#     plot_graph(axs, 1, "G_A", "Train", epochs, means[:, 2])
#     plot_graph(axs, 2, "cycle_A", "Train", epochs, means[:, 3])
#     plot_graph(axs, 3, "idt_A", "Train", epochs, means[:, 4])
#     plot_graph(axs, 4, "D_B", "Train", epochs, means[:, 5])
#     plot_graph(axs, 5, "G_B", "Train", epochs, means[:, 6])
#     plot_graph(axs, 6, "cycle_B", "Train", epochs, means[:, 7])
#     plot_graph(axs, 7, "idt_B", "Train", epochs, means[:, 8])

#     # Plotting
#     # FLYT UDKOMMENTERING WINDOWS/MAC STIER
#     # model = file_path.split("\\")[-2]
#     model = file_path.split("/")[-2]

#     title = f"{model}_plot"

#     fig.suptitle(title)

#     plt.tight_layout()
#     plt.savefig(f"{root_folder}/{title}.png") 
#     plt.close()


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
    #           
# def plot_graph(ax, ax_index, plot_label, x_vals, y_vals, line_color = "blue", plot_title = None):
#     if (plot_title):
#         ax[0, ax_index].set_title(plot_title)
#     ax[0, ax_index].grid(visible=True)
#     ax[0, ax_index].plot(x_vals, y_vals, label=plot_label, linewidth=1, color=line_color)
#     ax[0, ax_index].set_xlabel("Epoch")
#     ax[0, ax_index].set_ylabel("Loss")
#     ax[0, ax_index].legend()
#     ax[0, ax_index].spines['top'].set_visible(False)  # Hide the top spine for each subplot
#     ax[0, ax_index].spines['right'].set_visible(False)  # Hide the top spine for each subplot
#     ax[0, ax_index].yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.5, zorder=3)
#     ax[0, ax_index].set_facecolor('#f0f0f0')
    
    # if (plot_title):
    #     ax[1, ax_index].set_title(f"Smoothed {plot_title}")
    # ax[1, ax_index].grid(visible=True)
    # ax[1, ax_index].plot(x_vals, rolling_avg(y_vals,5), label=f"Smoothed {plot_label}", linewidth=0.5, color=line_color)
    # ax[1, ax_index].set_xlabel("Epoch")
    # ax[1, ax_index].set_ylabel("Loss")
    # ax[1, ax_index].legend()




def rolling_avg(a,n): 
    assert n%2==1
    b = a*0.0
    for i in range(len(a)) :
        b[i]=a[max(i-n//2,0):min(i+n//2+1,len(a))].mean()
    return b


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: gan_plot_losses.py <root folder>")

    else:

        print("Running gan_plot_losses.py")

        root_folder = sys.argv[1]

        log_files = find_log_files(os.path.join(root_folder,"Checkpoints"))

        for log in log_files:
            try:
                if (log.count("pix2pix")>0) or (log.count("g_nc")>0):
                    plot_log_p2p(log, root_folder)
                if (log.count("cycleGan")>0):
                    plot_log_cycleGan(log, root_folder)
            
            except IndexError:
                model = log.split("/")[-2]
                print(f"   gan_plot_losses.py caught exception: {model} probably needs to run longer")