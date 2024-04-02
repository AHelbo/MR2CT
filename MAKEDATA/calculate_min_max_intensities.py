import glob
import os
from PIL import Image
import nibabel 
import time
import sys
import shutil
from files2txt2files import read_list_from_file, save_list_to_file
import json
import numpy as np
import matplotlib.pyplot as plt


np_mr_arr = np.zeros((3001, 1))

np_ct_arr = np.zeros((4001, 1))

def nii_to_matrix_dict(folder, bad_data_file):

    bad_data = read_list_from_file(bad_data_file)

    partitions = [os.path.join(folder,dir) for dir in os.listdir(folder) if os.path.isdir(os.path.join(folder, dir))]
    for i, partition in enumerate(partitions):

        print(f"Starting work on partition \"{partition}\" ({i+1}/{len(partitions)})")

        #patient folders (some might not be..)
        patients = [os.path.join(partition,dir) for dir in os.listdir(partition) if (os.path.isdir(os.path.join(partition, dir)))]

        #enter each patient folder
        for patient in patients:

            patient_id = patient.split("/")[-1]
            print(f" Starting work on patient \"{patient_id}\"")
            os.chdir(patient) # I believe this is not needed

            #converts each scan of the patient individually
            for scan in glob.glob('*.nii.gz'):

                #we do not use the mask files so we delete then
                if scan == 'mask.nii.gz':
                    os.remove(scan)
                    continue

                #load the .nii.gz file
                nii = nibabel.load(scan)
                np_arr = np.asarray(nii.dataobj)

                for slice in range(np_arr.shape[2]):

                    if (f"{patient_id}-{slice:03}" in bad_data):
                        continue                    

                    # clean_arr.append(np_arr[:, :, slice])

                    #Minmaxnorm + scale as image
                    if (scan.split(".")[0] == "ct"):
                        for elm in np_arr[:, :, slice].flatten():
                            np_ct_arr[int(elm + 1000)] += 1
                        

                    if (scan.split(".")[0] == "mr"):    
                        for elm in np_arr[:, :, slice].flatten():
                            np_mr_arr[int(elm)] += 1

                del np_arr 
                del nii

def plot_mr():
    global np_mr_arr

    # Compute mean and standard deviation
    mean = np.mean(np_mr_arr)
    std_dev = np.std(np_mr_arr)
    
    # Plot mean
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=1, label='Mean')
    
    # Plot one standard deviation above and below the mean
    # plt.axvline(mean + std_dev, color='g', linestyle='dashed', linewidth=1, label='Mean ± 1 Std Dev')
    # plt.axvline(mean - std_dev, color='g', linestyle='dashed', linewidth=1)
    
    # Plot two standard deviations above and below the mean
    # plt.axvline(mean + 2*std_dev, color='b', linestyle='dashed', linewidth=1, label='Mean ± 2 Std Dev')
    # plt.axvline(mean - 2*std_dev, color='b', linestyle='dashed', linewidth=1)

    y_values = np.array(np_mr_arr)
    x_values = np.arange(len(y_values))
    plt.scatter(x_values, y_values)
    plt.xlabel('Intensity')
    plt.ylabel('Frequency)')
    plt.title('MR plot')
    plt.yscale('log')  # Set y-axis scale to logarithmic
    plt.grid(True)
    plt.show()

def plot_ct():
    global np_ct_arr

    # Compute mean and standard deviation
    mean = np.mean(np_ct_arr)
    std_dev = np.std(np_ct_arr)
    
    # Plot mean
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=1, label='Mean')
    
    # Plot one standard deviation above and below the mean
    # plt.axvline(mean + std_dev, color='g', linestyle='dashed', linewidth=1, label='Mean ± 1 Std Dev')
    # plt.axvline(mean - std_dev, color='g', linestyle='dashed', linewidth=1)
    
    # Plot two standard deviations above and below the mean
    # plt.axvline(mean + 2*std_dev, color='b', linestyle='dashed', linewidth=1, label='Mean ± 2 Std Dev')
    # plt.axvline(mean - 2*std_dev, color='b', linestyle='dashed', linewidth=1)

    y_values = np.array(np_ct_arr) + -1000
    # y_values = np.log(y_values)    
    x_values = np.arange(-1000, len(y_values) - 1000)
    plt.scatter(x_values, y_values)
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.title('CT plot')
    plt.yscale('log')  # Set y-axis scale to logarithmic
    plt.grid(True)
    plt.show()    

def histogram_ct(bins=20):
    global np_ct_arr

    # Compute mean and standard deviation
    mean = np.mean(np_ct_arr)
    std_dev = np.std(np_ct_arr)
    
    # Plot mean
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=1, label='Mean')
    
    # Plot one standard deviation above and below the mean
    # plt.axvline(mean + std_dev, color='g', linestyle='dashed', linewidth=1, label='Mean ± 1 Std Dev')
    # plt.axvline(mean - std_dev, color='g', linestyle='dashed', linewidth=1)
    
    # Plot two standard deviations above and below the mean
    plt.axvline(mean + 2*std_dev, color='b', linestyle='dashed', linewidth=1, label='Mean ± 2 Std Dev')
    plt.axvline(mean - 2*std_dev, color='b', linestyle='dashed', linewidth=1)

    plt.hist(np_ct_arr, bins=bins)
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.yscale('log')  # Set y-axis scale to logarithmic
    plt.grid(True)
    plt.show()

def histogram_mr(bins=20):
    global np_mr_arr

    # Compute mean and standard deviation
    mean = np.mean(np_mr_arr)
    std_dev = np.std(np_mr_arr)
    
    # Plot mean
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=1, label='Mean')
    
    # Plot one standard deviation above and below the mean
    # plt.axvline(mean + std_dev, color='g', linestyle='dashed', linewidth=1, label='Mean ± 1 Std Dev')
    # plt.axvline(mean - std_dev, color='g', linestyle='dashed', linewidth=1)
    
    # Plot two standard deviations above and below the mean
    plt.axvline(mean + 2*std_dev, color='b', linestyle='dashed', linewidth=1, label='Mean ± 2 Std Dev')
    plt.axvline(mean - 2*std_dev, color='b', linestyle='dashed', linewidth=1)

    plt.hist(np_mr_arr, bins=bins)
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.yscale('log')  # Set y-axis scale to logarithmic
    plt.grid(True)
    plt.show()    

def clean_folder(folder):
    dirs = [os.path.join(folder,dir) for dir in os.listdir(folder) if os.path.isdir(os.path.join(folder, dir))]

    for dir in dirs:
        shutil.rmtree(dir)

    zips = [os.path.join(folder,elm) for elm in os.listdir(folder) if elm.split(".")[-1] == "zip"]

    for z in zips:
        shutil.unpack_archive(z,folder)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 calculate.....py <path>")

    else:

        folder = sys.argv[1]

        bad = sys.argv[2]

        print("Removing existing unpacked data")
        clean_folder(folder)

        start = time.time()
        nii_to_matrix_dict("/Users/andershelbo/Desktop/MAKEDATA/Input_data", bad)
        end = time.time()

        print(f"nii_to_matrix_dict completed succesfully! Total time elapsed: {(end-start)/60} minutes")

        plot_mr()
        plot_ct()

        histogram_mr()
        histogram_ct()

        print(f"nifti2png has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")