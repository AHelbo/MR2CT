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
    pass

def process_gan_logs(logs):
    return process_logs(logs, process_gan_log)


def process_diffusion_logs(logs):
    return process_logs(logs, process_gan_log)
