import sys
from collections import defaultdict 
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import glob


def find_log_files(root_folder):
    
    search_pattern = os.path.join(root_folder, f"**/train.log")

    files = glob.glob(search_pattern, recursive=True)
    
    return files


def txt2dictPalette(txt_file):

    output_dict = defaultdict(dict)

    with open(txt_file, "r") as file:

        content = file.read()

        epochs = re.split(r'Validation End', content)

        for epoch in epochs:

            try:
                #find the epoch number
                epoch_number = re.split(" ", re.findall(r'epoch: .*\n', epoch)[0])[1]

                #find mean train/mse_loss
                tmp = re.findall(r'train\/mse_loss: .*\n', epoch)
                all_train_mse = [re.split(" ", tmp[i]) for i in range(len(tmp))]
                train_mse = [float(all_train_mse[i][1]) for i in range(len(all_train_mse))]

                #find other values to be plotted
                val_mae = re.split(" ", re.search(r'val\/mae: .*\n', epoch)[0])[1]
                val_mse = re.split(" ", re.search(r'val\/mse: .*\n', epoch)[0])[1]
                val_ssim = re.split(" ", re.search(r'val\/SSIM: .*\n', epoch)[0])[1]
                val_psnr = re.split(" ", re.search(r'val\/PSNR: .*\n', epoch)[0])[1]

                #add to dict
                output_dict[int(epoch_number)]['train_mse_loss'] = float(sum(train_mse)/len(train_mse))
                output_dict[int(epoch_number)]['val_mae'] = float(val_mae)
                output_dict[int(epoch_number)]['val_mse'] = float(val_mse)
                output_dict[int(epoch_number)]['val_SSIM'] = float(val_ssim)
                output_dict[int(epoch_number)]['val_PSNR'] = float(val_psnr)
            except: 
                pass

    return output_dict


def plot_dict_palette(output_dict, output_file, root_folder):
    epochs = output_dict.keys()

    train_mse_loss = np.array([output_dict[epoch]["train_mse_loss"] for epoch, _ in output_dict.items()])
    mae = np.array([output_dict[epoch]["val_mae"] for epoch, _ in output_dict.items()])
    mse = np.array([output_dict[epoch]["val_mse"] for epoch, _ in output_dict.items()])
    ssim = np.array([output_dict[epoch]["val_SSIM"] for epoch, _ in output_dict.items()])
    psnr = np.array([output_dict[epoch]["val_PSNR"] for epoch, _ in output_dict.items()])

    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplots(2, 4, figsize=(24, 8))


    plot_graph(axs, 0, "Train", epochs, train_mse_loss, line_color = "blue", plot_title = "MSE")    
    # plot_graph(axs, 0, "Val", epochs, mse, line_color = "orange")    

    plot_graph(axs, 1, "Val", epochs, ssim, line_color = "orange", plot_title = "SSIM")   

    plot_graph(axs, 2, "Val", epochs, mae, line_color = "orange", plot_title = "MAE")    

    plot_graph(axs, 3, "Val", epochs, psnr, line_color = "orange", plot_title = "PSNR")     


    model = output_file.replace("output_", "").split("/")[-2]

    title = f"{model}_plot"

    fig.suptitle(title)

    plt.tight_layout()
    plt.savefig(f"{root_folder}/{model}.png")
    plt.close()



def plot_graph(ax, ax_index, plot_label, x_vals, y_vals, line_color = "blue", plot_title = None):
    if (plot_title):
        ax[0, ax_index].set_title(plot_title)
    ax[0, ax_index].grid(visible=True)
    ax[0, ax_index].plot(x_vals, y_vals, label=plot_label, linewidth=0.5, color=line_color)
    ax[0, ax_index].set_xlabel("Epoch")
    ax[0, ax_index].set_ylabel("Loss")
    ax[0, ax_index].legend()
    
    if (plot_title):
        ax[1, ax_index].set_title(f"Smoothed {plot_title}")
    ax[1, ax_index].grid(visible=True)
    ax[1, ax_index].plot(x_vals, rolling_avg(y_vals,5), label=f"Smoothed {plot_label}", linewidth=0.5, color=line_color)
    ax[1, ax_index].set_xlabel("Epoch")
    ax[1, ax_index].set_ylabel("Loss")
    ax[1, ax_index].legend()


def rolling_avg(a,n): 
    assert n%2==1
    b = a*0.0
    for i in range(len(a)) :
        b[i]=a[max(i-n//2,0):min(i+n//2+1,len(a))].mean()
    return b


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_metrics.py <path to root folder>")
        
    else:

        print("Running palette_plot_losses.py")

        root_folder = sys.argv[1]

        log_files = find_log_files(os.path.join(root_folder,"Checkpoints"))

        for log in log_files:
            try:
                output_dict = txt2dictPalette(log)
                plot_dict_palette(output_dict, log, root_folder)

            except IndexError:
                model = log.split("/")[-2]
                print(f"   Caught exception: {model} probably needs to run longer")
            