import numpy as np
import nibabel as nib

# Load NIfTI file
nii_file_path = 'mr.nii.gz'
nii_img = nib.load(nii_file_path)

# Extract data as a 3D array
data = nii_img.get_fdata()

# Manipulate the data (e.g., adding 10 to each voxel)
modified_data = data + 10

# Create a new NIfTI image with the modified data
modified_nii_img = nib.Nifti1Image(modified_data, affine=nii_img.affine)

# Save the new NIfTI image to a file
output_nii_file_path = 'modified_example.nii.gz'
nib.save(modified_nii_img, output_nii_file_path)

print("Modified NIfTI file saved successfully.")