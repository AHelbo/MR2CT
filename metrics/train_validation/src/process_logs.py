import os
from src.utils import print_hierarchical
import numpy as np
import re
from collections import defaultdict

def process_logs(logs, func):
    dicts = []
    for log in logs:
        model_name = log.split("/")[-2]
        print_hierarchical(model_name,1)
        dicts.append((func(log), model_name))
    return dicts

def process_gan_log(log):

    accumulator_dict = defaultdict(lambda: defaultdict(list))

    with open(log, "r") as file:
        for line in file:
            if (line[0] == "="): 
                continue

            pattern = r'(\S+):\s*([\d\.]+)'

            pairs = re.findall(pattern, line)

            _, epoch = pairs[0]

            for pair in pairs[1:]:
                loss_name, loss =  pair
                accumulator_dict[epoch][loss_name].append(float(loss))

    mean_dict = defaultdict(lambda: defaultdict(float))

    for epoch, losses in accumulator_dict.items():
        for loss_name, loss in losses.items():
            mean_dict[epoch][loss_name] = sum(loss)/len(loss)

    return mean_dict

def process_diffusion_log(log):
    
    output_dict = defaultdict(dict)

    with open(log, "r") as file:

        content = file.read()

        epochs = re.split(r'Validation End', content)

        for epoch in epochs:
            try:
                #find the epoch number
                epoch_number = int(re.split(" ", re.findall(r'epoch: .*\n', epoch)[0])[1])
                if (epoch_number > 245):
                    continue 
                #find mean train/mse_loss
                tmp = re.findall(r'train\/mse_loss: .*\n', epoch)
                if (len(tmp) > 0):
                    all_train_mse = [re.split(" ", tmp[i]) for i in range(len(tmp))]
                    train_mse = np.mean([float(all_train_mse[i][1]) for i in range(len(all_train_mse))])
                    output_dict[epoch_number]['train_mse_loss'] = train_mse

                #find mean train/mae_loss
                tmp = re.findall(r'train\/mae_loss: .*\n', epoch)
                if (len(tmp) > 0):
                    all_train_mae = [re.split(" ", tmp[i]) for i in range(len(tmp))]
                    train_mae = np.mean([float(all_train_mae[i][1]) for i in range(len(all_train_mae))])
                    output_dict[epoch_number]['train_mae_loss'] = train_mae

                #find other values to be plotted
                val_mae = re.split(" ", re.search(r'val\/mae: .*\n', epoch)[0])[1]
                val_mse = re.split(" ", re.search(r'val\/mse: .*\n', epoch)[0])[1]
                val_ssim = re.split(" ", re.search(r'val\/SSIM: .*\n', epoch)[0])[1]
                val_psnr = re.split(" ", re.search(r'val\/PSNR: .*\n', epoch)[0])[1]
                
                val_step_mse = re.split(" ", re.search(r'val\/VAL_MSE: .*\n', epoch)[0])[1]

                #add to dict
                output_dict[epoch_number]['val_mae'] = float(val_mae)
                output_dict[epoch_number]['val_mse'] = float(val_mse)
                output_dict[epoch_number]['val_SSIM'] = float(val_ssim)
                output_dict[epoch_number]['val_PSNR'] = float(val_psnr)
                output_dict[epoch_number]['val_step_mse'] = float(val_step_mse)
            except:
                pass
    

    return output_dict

def process_gan_logs(logs):
    return process_logs(logs, process_gan_log)


def process_diffusion_logs(logs):
    return process_logs(logs, process_diffusion_log)
