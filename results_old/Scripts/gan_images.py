import sys
import os
import fnmatch
from PIL import Image, ImageDraw, ImageFont


def find_model_folders(root_dir):
    models = [os.path.join(root_dir, dir) for dir in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, dir))]
    return models


def concat_images(model_dir, root_dir):
    img_hw = 256
    text_h = 60
    
    image_dir = os.path.join(model_dir, "web", "images")

    epochs = set([int(elm.split("_")[0].split("epoch")[1]) for elm in os.listdir(image_dir) if elm.split(".")[-1] == "png"])
    epochs = sorted(epochs)
    epochs.reverse()

    if len(epochs) == 0:
        return
    
    # Create a list to store the images
    pdf_images = []

    for epoch in epochs:
        # Create a new image for each epoch
        epoch_image = Image.new("RGB", (3*img_hw, (text_h + img_hw)), color=(255, 255, 255))
        draw = ImageDraw.Draw(epoch_image)
        header_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 30)
        subheader_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 18)

        # Write epoch number and headers
        draw.text((1.5*img_hw-50, 5), f"Epoch {epoch}", font=header_font, fill=(0, 0, 0))
        draw.text((130, 40), f"Cond", font=subheader_font, fill=(0, 0, 0))
        draw.text((370, 40), f"GT", font=subheader_font, fill=(0, 0, 0))
        draw.text((600, 40), f"Out", font=subheader_font, fill=(0, 0, 0))

        y_offset = text_h

        cond = Image.open(os.path.join(image_dir, f"epoch{epoch:03}_real_A.png"))
        gt = Image.open(os.path.join(image_dir, f"epoch{epoch:03}_real_B.png"))
        out = Image.open(os.path.join(image_dir, f"epoch{epoch:03}_fake_B.png"))

        # Paste images onto the concatenated image
        epoch_image.paste(cond, (0, y_offset))
        epoch_image.paste(gt, (img_hw, y_offset))
        epoch_image.paste(out, (2*img_hw, y_offset))

        # Append the concatenated image to the list
        pdf_images.append(epoch_image)

    # Save the images as a PDF
    pdf_file_path = os.path.join(root_dir, f"{model_dir.split('/')[-1]}_images.pdf")
    pdf_images[0].save(pdf_file_path, save_all=True, append_images=pdf_images[1:])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 gan_images.py <path to root folder>")
        
    else:

        print("Running gan_images.py")

        root_folder = sys.argv[1]

        checkpoints_folder = os.path.join(root_folder, "Checkpoints", "GAN")

        model_folders = find_model_folders(checkpoints_folder)

        for model_folder in model_folders:
            try:
                concat_images(model_folder, root_folder)
            except FileNotFoundError:
                _, model = os.path.split(model_folder)
                print(f"   gan_images.py caught exception: {model} probably needs to run longer")
