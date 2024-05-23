import os
import sys
from PIL import Image

def resize_images(folder_path, output_size=(256, 256)):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is an image
        if filename.endswith(('.png')):
            # Construct the full path to the image file
            image_path = os.path.join(folder_path, filename)
            
            try:
                # Open the image using Pillow
                img = Image.open(image_path)
                
                # Resize the image
                resized_img = img.resize(output_size)
                
                # Save the resized image with the same name and path
                resized_img.save(image_path)
                
            except Exception as e:
                print(f"Failed to resize {filename}: {e}")

if __name__ == "__main__":
    # Check if a folder path is provided as argument
    if len(sys.argv) != 2:
        print("Usage: python resize.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        
        if not os.path.isdir(folder_path):
            print("Invalid folder path.")
        
        else:
            resize_images(folder_path)
