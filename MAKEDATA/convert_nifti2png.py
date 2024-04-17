import glob
import os
import nibabel 
import time
from PIL import Image
import sys
import shutil
from files2txt2files import read_list_from_file
import numpy as np

min_max_new_max = {}

def percentile_rank_limit(p_rank, p_limit):
    '''Takes the percentile rank arr of a single patient and returns 
    the cut-off value of the given percentile (the last intensity we should include)'''
    arg_lst = np.argwhere(p_rank >= p_limit)
    
    if len(arg_lst) == 0:
        return len(p_rank) - 1
    
    return arg_lst[0]

def cut_off_val(patient, p_limit):
    cumFreq = np.cumsum(patient)
    
    p_rank = (cumFreq - (0.5 * patient))/cumFreq[-1]*100

    limit_index = percentile_rank_limit(p_rank, p_limit)
    return limit_index[0]


def nifti2png(folder, bad_data_file):
    global min_max_new_max

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

                #make output dir for scan images
                outputdir = str.replace(scan, '.nii.gz', '')
                os.mkdir(outputdir)

                #load the .nii.gz file
                nii = nibabel.load(scan)
                niiArr = nii.get_fdata()

                #Minmaxnorm + scale as image
                if (scan.split(".")[0] == "ct"):
                    niiArr[niiArr > 2000] = 2000
                    niiArr[niiArr < -1000] = -1000

                if (scan.split(".")[0] == "mr"):
                    patient_mr_arr = np.zeros((3001))

                    for slice in range(niiArr.shape[2]):

                        if (f"{patient_id}-{slice:03}" in bad_data):
                            continue                    
                        
                        for elm in niiArr[:, :, slice].flatten():
                            patient_mr_arr[int(elm)] += 1

                    if (sum(patient_mr_arr) == 0): # if data is so bad that no data is left, just skip it.
                        print("  Frequency array empty, skipping..")
                        continue

                    val = cut_off_val(patient_mr_arr,98)

                    min_max_new_max[patient_id] = [niiArr.min(),niiArr.max(),val]

                    niiArr[niiArr > val] = val
                    niiArr[niiArr < 0] = 0                    

                # # Z-normalization
                # mean = np.mean(niiArr)
                # std_dev = np.std(niiArr)        
                # niiArr =(((niiArr - mean) / std_dev) * 255).astype('uint8')

                #make a .pgn image for each slice in the .nii file
                for slice in range(niiArr.shape[2]):

                    if (f"{patient_id}-{slice:03}" in bad_data):
                        continue

                    arr = niiArr[:, :, slice]

                    # MIN-MAX 
                    arr = ((arr - niiArr.min()) * (1/(niiArr.max() - niiArr.min()) * 255)).astype('uint8')

                    im = Image.fromarray(arr)

                    im.save(os.path.join(outputdir, f"image{slice:03}.png"))

                #delete .nii.gz file
                os.remove(scan)


def clean_folder(folder):
    dirs = [os.path.join(folder,dir) for dir in os.listdir(folder) if os.path.isdir(os.path.join(folder, dir))]

    for dir in dirs:
        shutil.rmtree(dir)

    zips = [os.path.join(folder,elm) for elm in os.listdir(folder) if elm.split(".")[-1] == "zip"]

    for z in zips:
        shutil.unpack_archive(z,folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 convert_nifti2png.py <path>")

    else:

        folder = sys.argv[1]

        bad_data_folder = sys.argv[2]
        
        start = time.time()

        print("Removing existing unpacked data")
        clean_folder(folder)

        print("Converting .nii files to .png")
        nifti2png(folder, bad_data_folder)

        print("limits:")
        for key, val in min_max_new_max.items():
            print(f"{key}: {val}")

        end = time.time()

        print(f"nifti2png has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")