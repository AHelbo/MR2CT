import tifffile
import numpy as np

def load_tiff_and_get_info(file_path):
    # Load the TIFF file
    with tifffile.TiffFile(file_path) as tif:
        # Read the image data
        image_data = tif.asarray()

    # Calculate relevant statistics
    min_val = np.min(image_data)
    max_val = np.max(image_data)
    mean_val = np.mean(image_data)
    std_val = np.std(image_data)
    shape = image_data.shape
    dtype = image_data.dtype

    # Return the statistics
    return {
        'min': min_val,
        'max': max_val,
        'mean': mean_val,
        'std': std_val,
        'shape': shape,
        'dtype': dtype
    }

# Example usage
file_path = '1BA125-027.tiff'  # Provide the correct file path
info = load_tiff_and_get_info(file_path)

# Print the information
for key, value in info.items():
    print(f'{key}: {value}')