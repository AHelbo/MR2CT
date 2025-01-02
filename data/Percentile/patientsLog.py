import glob
import os
import nibabel 
import time
import sys
import shutil
from files2txt2files import read_list_from_file
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

np_mr_arr = np.zeros((3001, 1))
np_ct_arr = np.zeros((4001, 1))

def nii_to_matrix_dict(target_folder, folder, bad_data_file):
    global np_ct_arr, np_mr_arr

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
                patient_ct_arr = np.zeros((4001, 1))
                patient_mr_arr = np.zeros((3001, 1))   

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

                    if (scan.split(".")[0] == "ct"):
                        for elm in np_arr[:, :, slice].flatten():
                            patient_ct_arr[int(elm + 1000)] += 1
                                    
                    if (scan.split(".")[0] == "mr"):
                        for elm in np_arr[:, :, slice].flatten():
                            patient_mr_arr[int(elm)] += 1
                
                #stack patient data to the full ct/mri arr
                if scan == 'ct.nii.gz':
                    np_ct_arr = np.column_stack((np_ct_arr, patient_ct_arr))

                if scan == 'mr.nii.gz':
                    np_mr_arr = np.column_stack((np_mr_arr, patient_mr_arr))

                del np_arr 
                del nii
            
    #remove the initial zero-column, and save as .csv file
    os.chdir(target_folder)
    np_ct_arr = np.delete(np_ct_arr, 0, 1)
    np_mr_arr = np.delete(np_mr_arr, 0, 1)
    # np_mr_arr.tofile('mr_intensities.csv', sep=',')
    # np_ct_arr.tofile('ct_intensities.csv', sep=',')
    

def plot_intensity(arr, modality):
    N = sum(arr)

    # Compute mean, fx, and plotted values based on modality
    if modality == 'CT':
        y_values = np.array(arr)
        x_values = np.arange(-1000, len(y_values) - 1000)
        mean = sum([(i-1000)*elm for i, elm in enumerate(arr)])/N
        fx = sum([(((x-1000)**2)*f) for x, f in enumerate(arr)])

    if modality == 'MR':
        y_values = np.array(arr)
        x_values = np.arange(len(y_values))
        mean = sum([i*elm for i, elm in enumerate(arr)])/N
        fx = sum([(((i)**2)*elm) for i, elm in enumerate(arr)])

    # plot std and more
    std = np.sqrt(fx/N-mean)
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=1, label='Mean')
    plt.axvline(mean+std, color='g', linewidth=1, label='1 std')
    plt.axvline(mean-std, color='g', linewidth=1, label='1 std')
    plt.axvline(mean+std*2, color='b', linewidth=1, label='2 std')
    plt.axvline(mean-std*2, color='b', linewidth=1, label='2 std')

    plt.scatter(x_values, y_values, s=1)
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.title(modality + ' plot')
    plt.yscale('log')  # Set y-axis scale to logarithmic
    plt.grid(True)
    plt.show()

def read_intensitylog(len, path, modality):
    print("1")
    print(path)
    np_log = (pd.read_csv(path, engine='c')).to_numpy()

    print("2")

    #reshaping the array to the modality intensity range
    np_log = np.delete(np.reshape(np_log, (len, -1)), 0, 1)
    print("3")

    plot_intensity(np.sum(np_log, axis=1), modality)
    print("4")

# read_intensitylog(4001, r'C:\Users\Emily Honey\MRI2CT\MAKEDATA\Input_data\brain\1BA005\ct_intensities.csv', 'CT')
# read_intensitylog(3001, r'C:\Users\Emily Honey\MRI2CT\MAKEDATA\Input_data\brain\1BA005\mr_intensities.csv', 'MR')

# nii_to_matrix_dict("/Users/andershelbo/Desktop/MRI2CT/MAKEDATA/Input_data","/Users/andershelbo/Desktop/MRI2CT/MAKEDATA/bad_data.txt")

def clean_folder(folder):
    dirs = [os.path.join(folder,dir) for dir in os.listdir(folder) if os.path.isdir(os.path.join(folder, dir))]

    for dir in dirs:
        shutil.rmtree(dir)

    zips = [os.path.join(folder,elm) for elm in os.listdir(folder) if elm.split(".")[-1] == "zip"]

    for z in zips:
        shutil.unpack_archive(z,folder)


def num_lines(path):
    with open(path, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting each data row one by one
        count = 0
        for row in csvreader:
            count += 1
        
        print(f"{count} rows in {path}")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 patiensLog.py < -load / -plot ")

    else:    
        if (sys.argv[1] == "-load"):

            script_dir = os.path.dirname(os.path.abspath(__file__))

            input_data_folder = os.path.join(script_dir, "Input_data")

            bad_data_file = os.path.join(script_dir, "bad_data.txt")
            
            start = time.time()

            print("..Removing existing unpacked data")
            clean_folder(input_data_folder)

            print("..writing patient intensities to file")
            nii_to_matrix_dict(script_dir, input_data_folder, bad_data_file)

            end = time.time()

            print(f"patientsLog.py has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")
        

        if (sys.argv[1] == "-plot"):

            script_dir = os.path.dirname(os.path.abspath(__file__))

            # read_intensitylog(4001, os.path.join(script_dir, "ct_intensities.csv"), 'CT')

            # read_intensitylog(3001, os.path.join(script_dir, "mr_intensities.csv"), 'MR')

            num_lines(os.path.join(script_dir, "ct_intensities.csv"))

            num_lines(os.path.join(script_dir, "mr_intensities.csv"))

            num_lines(os.path.join(script_dir, "test.csv"))



            

            