import sys
import os
import glob
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def find_log_files(root_folder):
    
    search_pattern = os.path.join(root_folder, f"**/loss_log.txt")

    files = glob.glob(search_pattern, recursive=True)
    
    return files

def plot_log_cycleGan(file_path, root_folder):
    data = []


    with open(file_path, "r") as file:
        for line in file:
            if (line[0] == "="):
                continue

            # Splitting each line by spaces
            parts = line.replace(":",",").replace(" ",",").split(",")
            # for i, elm in enumerate(parts):
            #     print(f"{i} {elm}")
            # Extracting relevant information
            epoch = int(parts[2])
            D_A = float(parts[17])
            G_A = float(parts[20])
            cycle_A = float(parts[23])
            idt_A = float(parts[26])
            D_B = float(parts[29])
            G_B = float(parts[32])
            cycle_B = float(parts[35])
            idt_B = float(parts[38])


            # Appending to data
            data.append([epoch, D_A, G_A, cycle_A, idt_A, D_B, G_B, cycle_B, idt_B])
    data = np.array(data)

    epochs = np.unique(data[:,0])

    means = []
    for value in epochs:
        mask = data[: , 0] == value
        subset = data[mask]
        D_A = np.mean(subset[:, 1])
        G_A = np.mean(subset[:, 2])
        cycle_A = np.mean(subset[:, 3])
        idt_A = np.mean(subset[:, 4])
        D_B = np.mean(subset[:, 5])
        G_B = np.mean(subset[:, 6])
        cycle_B = np.mean(subset[:, 7])
        idt_B = np.mean(subset[:, 8])
        means.append([value, D_A, G_A, cycle_A, idt_A, D_B, G_B, cycle_B, idt_B])
    means = np.array(means)

    data_dict = {}
    data_dict["D_A"] = np.column_stack((epochs, means[:, 1]))
    data_dict["G_A"] = np.column_stack((epochs, means[:, 2]))
    data_dict["cycle_A"] = np.column_stack((epochs, means[:, 3]))
    data_dict["idt_A"] = np.column_stack((epochs, means[:, 4]))
    data_dict["D_B"] = np.column_stack((epochs, means[:, 5]))
    data_dict["G_B"] = np.column_stack((epochs, means[:, 6]))
    data_dict["cycle_B"] = np.column_stack((epochs, means[:, 7]))
    data_dict["idt_B"] = np.column_stack((epochs, means[:, 8]))

    # Plotting
    model = file_path.split("/")[-2]
    title = f"{model}_training_progress"

    harry_plotter(data_dict, root_folder, title)


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
            # if (len(parts) > 30):
            #     val_G_GAN = float(parts[29])
            #     val_G_L1 = float(parts[32])
            # else:
            #     val_G_GAN = 0.0
            #     val_G_L1 = 0.0

            # Appending to data
            data.append([epoch, G_GAN, G_L1, D_real, D_fake, val_G_GAN, val_G_L1])
    
    data = np.array(data)
    epochs = np.unique(data[:,0])[:-1] #We don't want the most recent epoch, as it may be unreliable

    if (len(epochs) == 0):
        pass

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
        
        means.append([value, mean_G_GAN, mean_G_L1, mean_D_real, mean_D_fake, mean_val_G_GAN, mean_val_G_L1])
    means = np.array(means)

    data_dict = {}
    data_dict["G_GAN"] = np.column_stack((epochs, means[:, 1]))
    data_dict["G_L1"] = np.column_stack((epochs, means[:, 2]))
    data_dict["D_real"] = np.column_stack((epochs, means[:, 3]))
    data_dict["D_fake"] = np.column_stack((epochs, means[:, 4]))
    data_dict["val_G_GAN"] = np.column_stack((epochs, means[:, 5]))
    data_dict["val_G_L1"] = np.column_stack((epochs, means[:, 6]))

    # Plotting
    model = file_path.split("/")[-2]
    title = f"{model}_training_progress"

    harry_plotter(data_dict, root_folder, title)
    
def rolling_avg(a,n): 
    assert n%2==1
    b = a*0.0
    for i in range(len(a)) :
        b[i]=a[max(i-n//2,0):min(i+n//2+1,len(a))].mean()
    return b

def harry_plotter(data_dict, root_folder, title):
    
    fig, axs = plt.subplots(2, len(data_dict), figsize=(6*len(data_dict), 2*len(data_dict)))

    smoothed_data = {key: rolling_avg(VALue[:,1], 5) for key, VALue in data_dict.items()}

    for i, (loss, vals) in enumerate([(key, value) for key, value in data_dict.items() if "val" not in key]):
        x_values = vals[:,0]
        y_values = vals[:,1]
        axs[0,i].plot(x_values, y_values, marker='o', linestyle='-', markersize = 2)
        axs[0,i].set_title(f"{loss}")
        axs[0,i].set_xlabel("Epoch")
        axs[0,i].set_ylabel(f"{loss}")

        axs[1,i].plot(x_values, smoothed_data[loss])
        axs[1,i].set_xlabel("Epoch")
        axs[1,i].set_ylabel(f"Rolling average ({loss})")        

    fig.suptitle(title)
    plt.tight_layout()
    plt.savefig(f"{root_folder}/{title}.png") 


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: _____")

    else:

        print("Running plot_losses.py")

        root_folder = sys.argv[1]

        log_files = find_log_files(root_folder)

        for log in log_files:
            if (log.count("pix2pix")>0):
                plot_log_p2p(log, root_folder)
            if (log.count("cycleGan")>0):
                plot_log_cycleGan(log, root_folder)
