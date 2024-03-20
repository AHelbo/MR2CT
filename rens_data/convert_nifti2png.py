import glob
import os
import nibabel 
import time
from PIL import Image
import sys
import shutil

def nifti2png(folder):

    partitions = [os.path.join(folder,dir) for dir in os.listdir(folder) if os.path.isdir(os.path.join(folder, dir))]

    for partition in partitions:

        print(f"Starting work on partition \"{partition}\":")

        #patient folders (some might not be..)
        patients = os.listdir(partition)

        #enter each patient folder
        for patient in patients:

            print(f" Starting work on patient \"{patient}\"")

            #check that we only treat folders. If its not a fodler we skip!
            if not os.path.isdir(os.path.join(partition, patient)):
                continue
            
            patient = os.path.join(partition, patient)
            os.chdir(patient)

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
                    
                #make a .pgn image for each slice in the .nii file
                for slice in range(niiArr.shape[2]):
                                                
                    arr = niiArr[:, :, slice]

                    ####### normalization happens here

                    arr = ((arr - niiArr.min()) * (1/(niiArr.max() - niiArr.min()) * 255)).astype('uint8')

                    im = Image.fromarray(arr)

                    im.save(os.path.join(outputdir, f"image{slice:03}.jpeg"))

                #delete .nii.gz file
                os.remove(scan)

        print(f" Partition \"{partition}\" is done")


def clean_folder(folder):
    dirs = [os.path.join(folder,dir) for dir in os.listdir(folder) if os.path.isdir(os.path.join(folder, dir))]

    for dir in dirs:
        shutil.rmtree(dir)

    zips = [os.path.join(folder,elm) for elm in os.listdir(folder) if elm.split(".")[-1] == "zip"]

    for z in zips:
        shutil.unpack_archive(z,folder)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 convert_nifti2png.py <path>")

    else:

        path = sys.argv[1]
        
        start = time.time()

        print("Removing existing unpacked data")
        clean_folder(path)

        nifti2png(path)

        end = time.time()

        print(f"nifti2png has been completed succesfully! Total time elapsed: {(end-start)/60} minutes")