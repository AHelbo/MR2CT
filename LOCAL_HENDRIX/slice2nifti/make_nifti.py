import sys
import os
import shutil
from collections import defaultdict
import numpy as np
from PIL import Image
from functools import partial
import glob
import nibabel
from scipy.interpolate import interpn
from scipy.ndimage import zoom



# givet input_test
# lav en dict med hver patient fra test-mappen, hvor val er et np array
def create_patient_dict(model_results_folder, img_type):
    patient_dict = {}

    slices = [elm for elm in os.listdir(model_results_folder) if elm[-10:] == f"{img_type}_B.png"]
    slices.sort()

    for slice in slices[:171]:

        pid = slice.split("-")[0]

        image_path = os.path.join(model_results_folder,slice)
        slice_arr = np.asarray(Image.open(image_path).convert('L'))

        if pid not in patient_dict:
            # Initialize with a new dimension for stacking
            patient_dict[pid] = np.expand_dims(slice_arr, axis=2)
        else:
            # Stack along the third dimension
            patient_dict[pid] = np.concatenate((patient_dict[pid], np.expand_dims(slice_arr, axis=2)), axis=2)


    return patient_dict

# givet dict med patienter, find den tilsvarende ct-fil i input_make-mappen, og genskab nifti-filter
# output i ny mappe som modellensnavn/pid.nii. bash laver mappen
def create_nifti(patient_dict, nifti_input_folder, output_folder):
    
    for pid, arr in patient_dict.items():
        print(pid)
        # Map back to ct image range [-1000,2000]
        arr = (arr.astype(float) / 255 * 3000 - 1000)

        # We need the header, and affine matrix from an original nifti-file        
        original_scan = glob.glob(f"{nifti_input_folder}/*/{pid}/ct.nii.gz")[0]
        nii_original_scan = nibabel.load(original_scan)

        nii_original_scan.header["dim"][1] = arr.shape[0]
        nii_original_scan.header["dim"][2] = arr.shape[1]
        nii_original_scan.header["dim"][3] = arr.shape[2]

        # print(nii_original_scan.header)

        print(np.array(nii_original_scan.get_fdata()).shape)

        og_arr = nii_original_scan.get_fdata()


        new_nifti = nibabel.Nifti1Image(arr, nii_original_scan.affine)
        print(np.array(new_nifti.get_fdata()).shape)

        nibabel.save(new_nifti, f"{output_folder}/{pid}.nii.gz")


        arr = resize_matrix(arr, og_arr, 3)
        print(arr.shape)

        

def resize_matrix(matrix, target_shape, interpolation_order=3):
    zoom_factors = [float(target) / original for target, original in zip(target_shape, matrix.shape)]
    
    # Resize the matrix using the computed zoom factors
    resized_matrix = zoom(matrix, zoom_factors, order=interpolation_order)
    
    return resized_matrix


def create_crosssection(patient_dict, output_folder, img_type):
    for pid, arr in patient_dict.items():
        n = int(arr.shape[0]/2)
        im = Image.fromarray(arr[n, :, :])
        im  = im.resize((256,256))
        im.save(f"{os.path.join(output_folder,pid)}-{img_type}.png")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 palette_images.py <path to folder containing original nifti files> <path to model output> <path to output folder>")
        
    else:

        # input1 = input-mappe fra MAKE_DATA
        nifti_input_folder = sys.argv[1]
        # input_test = mappe med cond, gt og out - den mappe som modellerne allerede producerer
        model_results_folder = sys.argv[2]
        # out_folder = ...
        output_folder = sys.argv[3]   

        fake_patient_dict = create_patient_dict(model_results_folder,"fake")
        # real_patient_dict = create_patient_dict(model_results_folder,"real")

        create_nifti(fake_patient_dict, nifti_input_folder, output_folder)

        # create_crosssection(fake_patient_dict, output_folder, "fake")
        # create_crosssection(real_patient_dict, output_folder, "real")