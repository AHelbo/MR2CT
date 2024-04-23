import sys
from collections import defaultdict 
import matplotlib.pyplot as plt
import numpy as np
import re


def txt2dictPalette(txt_file):

    output_dict = defaultdict(dict)

    with open(txt_file, "r") as file:

        content = file.read()

        epochs = re.split(r'Validation End', content)

        for epoch in epochs:
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

    return output_dict

def plot_dict_palette(output_dict, output_file):
    epochs = output_dict.keys()

    train_mse_loss = np.array([output_dict[epoch]["train_mse_loss"] for epoch, _ in output_dict.items()])
    mae = np.array([output_dict[epoch]["val_mae"] for epoch, _ in output_dict.items()])
    mse = np.array([output_dict[epoch]["val_mse"] for epoch, _ in output_dict.items()])
    ssim = np.array([output_dict[epoch]["val_SSIM"] for epoch, _ in output_dict.items()])
    psnr = np.array([output_dict[epoch]["val_PSNR"] for epoch, _ in output_dict.items()])

    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplots(2, 5, figsize=(24, 8))

    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "val_SSIM",
        0,
        epochs, 
        [
            {"label" : "SSIM", "legend" : "legend", "values" : ssim, "color" : "blue"},
        ])        

    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "train_mse_loss",
        1,
        epochs, 
        [
            {"label" : "PSNR", "legend" : "legend", "values" : train_mse_loss, "color" : "blue"},
        ])  
    
    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "MAE",
        2,
        epochs, 
        [
            {"label" : "MAE", "legend" : "legend", "values" : mae, "color" : "blue"},
        ])  
    
    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "MSE",
        3,
        epochs, 
        [
            {"label" : "MSE", "legend" : "legend", "values" : mse, "color" : "blue"},
        ])          

    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "PSNR",
        4,
        epochs, 
        [
            {"label" : "PSNR", "legend" : "legend", "values" : psnr, "color" : "blue"},
        ])     

    model = output_file.replace("output_", "")

    title = f"{model}_training_progress"

    fig.suptitle(title)

    plt.tight_layout()
    plt.savefig(f"{title}.png")

def harry_plotter_and_the_chamber_of_plots(ax, title, index, x_val, y_values):
    for y_val in y_values:
        ax[0, index].grid(visible=True)
        ax[0, index].set_title(title)
        ax[0, index].plot(x_val, y_val["values"], label=y_val["label"], linewidth=0.5, color=y_val["color"])
        ax[0, index].set_xlabel("Epoch")
        ax[0, index].set_ylabel("Loss")
        ax[0, index].legend()

        ax[1, index].grid(visible=True)
        ax[1, index].set_title(f"Smoothed {title}")
        ax[1, index].plot(x_val, rolling_avg(y_val["values"],5), label=f"Smoothed", linewidth=0.5, color=y_val["color"])
        ax[1, index].set_xlabel("Epoch")
        ax[1, index].set_ylabel("Loss")
        ax[1, index].legend()

def rolling_avg(a,n): 
    assert n%2==1
    b = a*0.0
    for i in range(len(a)) :
        b[i]=a[max(i-n//2,0):min(i+n//2+1,len(a))].mean()
    return b

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot_metrics.py <path to output file>")

    else:
        output_file = sys.argv[1]
        output_dict = txt2dictPalette(output_file)
        plot_dict_palette(output_dict, output_file)