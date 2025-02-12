import sys
from collections import defaultdict 
import matplotlib.pyplot as plt
import numpy as np

def txt2dict(txt_file):
    
    output_dict = defaultdict(dict) 
    
    with open(txt_file, "r") as file:        
        for line in file:
            # We need to handle incomplete ouput files, ie. missing metrics or metric values
            try:
                _, epoch, metric, metric_value = line.replace("\n","").split(" ")
                output_dict[int(epoch)][metric] = float(metric_value)
            except ValueError:
                # missing metrics are either empty or strings of text, neither can be cast to float. We just skip it and reove the wntire epoch later
                pass

    # Remove epochs that do not have all metrics:
    output_dict = {epoch: metrics for epoch, metrics in output_dict.items() if len(metrics) == 6}

    sorted_dict = dict(sorted(output_dict.items()))

    return sorted_dict


def plot_dict(output_dict, output_file):
    
    epochs = output_dict.keys()

    plt.style.use('default')
    fig, axs = plt.subplots(2, 4, figsize=(24, 8))

    # for i, metric in enumerate(["MAE","MSE","SSIM","PSNR","SIMOS","FID"]):
    for i, metric in enumerate(["SSIM","PSNR","SIMOS","FID"]):
        metrics = np.array([output_dict[epoch][metric] for epoch, _ in output_dict.items()])
        plot_graph(axs, i, "Val data", epochs, metrics, line_color = "orange", plot_title = metric)

    model = output_file.replace("output_", "").replace(".txt", "")

    title = f"{model}"

    fig.suptitle(title)

    plt.tight_layout()
    plt.savefig(f"{title}.png")   


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

def plot_pretty_graph(ax, ax_index, plot_label, x_vals, y_vals, line_color = "blue", plot_title = None):
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
        print("Usage: python3 plot_metrics.py <path to output file>")

    else:
        output_file = sys.argv[1]

        output_dict = txt2dict(output_file)

        plot_dict(output_dict, output_file)
