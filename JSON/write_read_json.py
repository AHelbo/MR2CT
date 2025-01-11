
import random
import json
from collections import defaultdict


epoch_data_points = []

for i in range(15):
    epoch_data_points.append(
        {
            "epoch": i,
            "loss1": (random.random()),
            "loss2": (random.random()),
            "loss3": (random.random()),
            "loss4": (random.random()),
        }
    )


# for data_points in epoch_data_points:
    
#     output = ''
#     for key, val in data_points.items():
#         output += '%s: %d, ' % (key, val)

#     out_file = open("data.txt", "a")

#     out_file.write('%s\n' % output[:-2])




import numpy as np 

losses = defaultdict(lambda: defaultdict(lambda: np.zeros((0,))))

# load
with open("data.txt", "r") as file:
    for line in file:
        datapoints = line.split(',')

        print(datapoints)

        _, epoch = datapoints[0].replace(" ","").split(":")

        for datapoint in datapoints[1:]:

            key, val = datapoint.replace(" ","").split(":")

            losses[epoch][key] += val

# mean

print(losses)
            
