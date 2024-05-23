import sys
from collections import defaultdict 
import matplotlib.pyplot as plt
import numpy as np

def txt2dict(txt_file):
    
    output_dict = defaultdict(dict) 
    
    with open(txt_file, "r") as file:        

        for line in file:
            parts = line.replace("\n","").split(" ")
            output_dict[int(parts[1])][parts[2]] = float(parts[3])

    sorted_dict = dict(sorted(output_dict.items()))

    return sorted_dict

def plot_dict(output_dict, output_file):
    
    epochs = output_dict.keys()

    ssim = np.array([output_dict[epoch]["SSIM"] for epoch, _ in output_dict.items()])
    psnr = np.array([output_dict[epoch]["PSNR"] for epoch, _ in output_dict.items()])
    mae = np.array([output_dict[epoch]["MAE"] for epoch, _ in output_dict.items()])
    mse = np.array([output_dict[epoch]["MSE"] for epoch, _ in output_dict.items()])
    fid = np.array([output_dict[epoch]["FID"] for epoch, _ in output_dict.items()])
    simos = np.array([output_dict[epoch]["SIMOS"] for epoch, _ in output_dict.items()])

    plt.style.use('seaborn-v0_8')
    fig, axs = plt.subplots(2, 6, figsize=(24, 8))

    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "SSIM",
        0,
        epochs, 
        [
            {"label" : "ssim", "legend" : "legend", "values" : ssim, "color" : "blue"},
        ])        

    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "PSNR",
        1,
        epochs, 
        [
            {"label" : "psnr", "legend" : "legend", "values" : psnr, "color" : "blue"},
        ])  
    
    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "MAE",
        2,
        epochs, 
        [
            {"label" : "mae", "legend" : "legend", "values" : mae, "color" : "blue"},
        ])  
    
    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "MSE",
        3,
        epochs, 
        [
            {"label" : "mse", "legend" : "legend", "values" : mse, "color" : "blue"},
        ])          

    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "FID",
        4,
        epochs, 
        [
            {"label" : "fid", "legend" : "legend", "values" : fid, "color" : "blue"},
        ])     

    harry_plotter_and_the_chamber_of_plots(
        axs, 
        "SIMOS",
        5,
        epochs, 
        [
            {"label" : "fid", "legend" : "legend", "values" : simos, "color" : "blue"},
        ])     

    model = output_file.replace("output_", "").replace(".txt", "")

    title = f"{model}"

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

        output_dict = txt2dict(output_file)

        plot_dict(output_dict, output_file)
