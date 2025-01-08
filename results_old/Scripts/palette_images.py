import sys
import os
import fnmatch
from PIL import Image, ImageDraw, ImageFont


def find_train_folders(root_dir):
    train_folders = []
    for root, dirs, _ in os.walk(root_dir):
        for dir_name in dirs:
            if fnmatch.fnmatch(dir_name, "train_*"):
                train_folders.append(os.path.join(root, dir_name))
    return train_folders


def concat_images(exp_dir, root_dir):

    cols = 8
    img_hw = 224
    text_h = 50
    buffer_w = 10
    
    val_dir = os.path.join(exp_dir,"results", "val")
    epochs = sorted([int(elm) for elm in os.listdir(val_dir) if os.path.isdir(os.path.join(val_dir, elm))])
    epochs.reverse()
    
    pdf_images = []

    for epoch in epochs:
        
        epoch_image = Image.new("RGB", (cols*3*img_hw+(cols-1)*buffer_w, (text_h + img_hw)), color = (255, 255, 255)) 

        # Create text-block
        img = Image.new("RGB", (cols*(img_hw*3+buffer_w), text_h), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        header_fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", 30)
        subheader_fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", 18)

        # Write what epoch is depicted
        d.text((cols*(img_hw*3+buffer_w)*.5-50,0), f"Epoch {epoch}", font=header_fnt, fill=(0,0,0))

        
        # Annotate with cond, gt, out
        for i in range(cols):

            x_offset = i*(3*img_hw+buffer_w)
            
            d.text((x_offset+90,30), f"Cond", font = subheader_fnt, fill=(0,0,0))
            d.text((x_offset+320,30), f"GT", font = subheader_fnt, fill=(0,0,0))
            d.text((x_offset+550,30), f"Out", font = subheader_fnt, fill=(0,0,0))

        epoch_image.paste(img, (0, 0))

        y_offset = text_h

        GT_imgs = sorted([elm for elm in os.listdir(os.path.join(val_dir, f"{epoch}")) if elm.split("_")[0] == "GT"])

        if (len(GT_imgs) < 8):
            continue

        for i in range(len(GT_imgs)):

            gt = GT_imgs[i]
            out = "Out_" + gt.split("_")[1]
            cond = "cond_" + gt.split("_")[1]

            gt_img = Image.open(os.path.join(val_dir,str(epoch),gt))
            out_img = Image.open(os.path.join(val_dir,str(epoch),out))
            cond_img = Image.open(os.path.join(val_dir,str(epoch),cond))

            # concate images here
            x_offset = i * (3 * img_hw + buffer_w)    
            epoch_image.paste(cond_img, (x_offset + 0*img_hw, y_offset))
            epoch_image.paste(gt_img, (x_offset + 1*img_hw, y_offset))
            epoch_image.paste(out_img, (x_offset + 2*img_hw, y_offset))
        
        pdf_images.append(epoch_image)

    pdf_file_path = os.path.join(root_dir, f"{exp_dir.split('/')[-1]}_images.pdf")
    pdf_images[0].save(pdf_file_path, save_all=True, append_images=pdf_images[1:])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 palette_images.py <path to root folder>")
        
    else:

        print("Running palette_images.py")

        root_folder = sys.argv[1]

        checkpoints_folder = os.path.join(root_folder, "Checkpoints")

        experiment_folders = find_train_folders(checkpoints_folder)

        for exp_folder in experiment_folders:
            try:
                concat_images(exp_folder, root_folder)

            except FileNotFoundError:
                _, model = os.path.split(exp_folder)
                print(f"   palette_images.py caught FileNotFoundError exception: {model} probably needs to run longer")

            except:
                _, model = os.path.split(exp_folder)
                print(f"   palette_images.py caught exception: {model} probably needs to run longer")                