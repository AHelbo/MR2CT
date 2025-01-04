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

    cols = 2
    img_hw = 224
    
    val_dir = os.path.join(exp_dir,"results", "val")
    epochs = sorted([int(elm) for elm in os.listdir(val_dir) if os.path.isdir(os.path.join(val_dir, elm))])
    
    concatenated_image = Image.new("RGB", (cols*3*img_hw+(cols-1), img_hw * len(epochs)), color = (255, 255, 255)) # mangler plads til epoch-billedet

    y_offset = 0

    for epoch in epochs:
        
        GT_imgs = sorted([elm for elm in os.listdir(os.path.join(val_dir, f"{epoch}")) if elm.split("_")[0] == "GT"])

        for i in range(len(GT_imgs)):

            gt = GT_imgs[i]
            out = "Out_" + gt.split("_")[1]
            cond = "cond_" + gt.split("_")[1]

            gt_img = Image.open(os.path.join(val_dir,str(epoch),gt))
            out_img = Image.open(os.path.join(val_dir,str(epoch),out))
            cond_img = Image.open(os.path.join(val_dir,str(epoch),cond))

            # concate images here
            x_offset = i * 3 * img_hw    
            concatenated_image.paste(cond_img, (x_offset + 0*img_hw, y_offset))
            concatenated_image.paste(gt_img, (x_offset + 1*img_hw, y_offset))
            concatenated_image.paste(out_img, (x_offset + 2*img_hw, y_offset))
        
        y_offset += img_hw

    name = exp_dir.split("/")[-1]
    concatenated_image.save(os.path.join(root_dir, f"{name}_training_progress.jpg"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 palette_images.py <path to root folder>")
        
    else:

        print("Running palette_images.py")

        root_folder = sys.argv[1]

        checkpoints_folder = os.path.join(root_folder, "Checkpoints")

        experiment_folders = find_train_folders(checkpoints_folder)

        for exp_folder in experiment_folders:
            concat_images(exp_folder, root_folder)
