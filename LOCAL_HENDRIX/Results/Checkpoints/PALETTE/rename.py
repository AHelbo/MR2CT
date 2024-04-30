import os
import glob

def rename_files(folder_path):
    # Get all files matching the pattern cond_*
    files = glob.glob(f'{folder_path}/*/*/*/*/cond_*')

    for file_path in files:

        path, file_name = os.path.split(file_path)

        # Construct the new file name with 'Cond_' prefix
        new_file_name = 'Cond_' + file_name[5:]

        # Construct the new file path
        new_file_path = os.path.join(path, new_file_name)

        # Rename the file
        os.rename(file_path, new_file_path)
        print(f"Renamed {file_path} to {new_file_path}")

# Provide the folder path here
folder_path = '/Users/andershelbo/Desktop/MR2CT/LOCAL_HENDRIX/Results/Checkpoints/PALETTE'

# Call the function to rename files
rename_files(folder_path)