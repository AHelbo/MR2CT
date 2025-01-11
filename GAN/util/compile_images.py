import os
from PIL import Image, ImageDraw, ImageFont
from time import time
from tifffile import imread
import numpy as np

COLUMNS = 8
PADDING = 5
IMG_HW = 256
EPOCH_H = 100
SET_PADDING = 20
SET_H = EPOCH_H + IMG_HW 
SET_W = PADDING * 3 + IMG_HW * 3

def tiff_to_pil(img_path):
    tiff_img = np.array(imread(img_path))  # [0,1]
    reg_img = (tiff_img * 255).astype(np.uint8)
    return Image.fromarray(reg_img)

def concat_images(exp_dir):
    val_dir = os.path.abspath(os.path.join(exp_dir, "results", "val"))
    epochs = sorted([int(elm) for elm in os.listdir(val_dir) if os.path.isdir(os.path.join(val_dir, elm))], reverse=True)
    pdf_images = []
    header_fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", 30)
    subheader_fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", 12)

    for epoch in epochs:
        epoch_image = Image.new("RGB", (COLUMNS * SET_W + (COLUMNS - 1) * SET_PADDING + 2 * SET_PADDING, SET_H + PADDING), color=(26, 26, 26))
        d = ImageDraw.Draw(epoch_image)
        d.text((COLUMNS * SET_W * .5, EPOCH_H * .32), f"EPOCH {epoch}", font=header_fnt, fill=(255, 255, 255))
        
        img_names = sorted([elm.split("_")[1] for elm in os.listdir(os.path.join(val_dir, f"{epoch}")) if elm.split("_")[0] == "GT"])
        
        if len(img_names) < COLUMNS:
            continue

        for i in range(COLUMNS):
            labels = [f"cond_{img_names[i]}", f"GT_{img_names[i]}", f"Out_{img_names[i]}"]
            imgs = [tiff_to_pil(os.path.join(val_dir, str(epoch), label)) for label in labels]

            for j, img, label in zip(range(3), imgs, labels):
                set_offset = i * 3 * (PADDING + IMG_HW) + i * SET_PADDING + SET_PADDING
                img_offset = j * (PADDING + IMG_HW)
                x_offset = set_offset + img_offset
                y_offset = EPOCH_H
                epoch_image.paste(img, (x_offset, y_offset))
                d.text((x_offset + IMG_HW * .28, y_offset + IMG_HW * .92), label, font=subheader_fnt, fill=(255, 255, 255))

        pdf_images.append(epoch_image)

    if pdf_images:
        pdf_file_path = os.path.join(exp_dir, f"{os.path.basename(exp_dir)}_epochs.pdf")
        pdf_images[0].save(pdf_file_path, save_all=True, append_images=pdf_images[1:])

def compile_images(checkpoint_dir):
        try:
            concat_images(checkpoint_dir)

        except Exception as e:
            print(f"failed to compile images: {e}")