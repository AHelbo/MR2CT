from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from PIL import Image 
import torchvision.transforms as transforms 
import torch 
import cv2
import numpy as np
import sys
import os
import glob
import regex as re

def image2Mask(path):
    #read a 2D image as required for the SAM segmentator
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return mask_generator.generate(img)

def IoU(gt_masks, fake_masks):
    #calculates the intersect of unions on of the fake and the ground truth masks 
    ret = 0

    for gt_mask in gt_masks:
        bestIoU = 0
        for fake_mask in fake_masks:
            intersect = np.logical_and(fake_mask["segmentation"], gt_mask["segmentation"])
            union = np.logical_or(fake_mask["segmentation"], gt_mask["segmentation"])
            iou = np.sum(intersect)/np.sum(union)            
            if bestIoU < iou:
                bestIoU = iou
        ret += bestIoU
    return ret/len(gt_masks)

def totalIoU(data_folder):
    #calculates the total IoU of an entire datafolder (folder must contain real and fake img)

    #file will be at the same dir as the datafolder, contains info of each img IoU
    f = open("IoU.txt", "w")
    os.chdir(data_folder)

    #acc of IoU and img pairs (not all img has synthetic counterparts in folder)
    sumIoU = 0
    nPairs = 0

    for scan in glob.glob('*.png'):
        
        #if the image is real and it has a corresponding synthetic image, we calculate IoU
        if re.search(r"real", scan) != None:
            fake = re.sub(r"real", "fake", scan)
            if os.path.exists(fake):
                gt_mask = image2Mask(scan)
                fake_mask = image2Mask(fake)

                currIoU = IoU(gt_mask, fake_mask)

                f.write(f"patientID={scan}, IoU={currIoU}, gt_masks={len(gt_mask)}, fake_masks={len(fake_mask)}\n")            

                sumIoU += currIoU
                nPairs += 1

    f.write(f"totalIoU={sumIoU/nPairs}\n")

    f.close()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Wrong number of arguments - you can do better")

    else:
        #define varibale from cmd-line
        data_folder = sys.argv[1]

        #path to the model checkpoint and definition of the model
        print("Loading SAM")
        checkpoint = sys.argv[2]
        sam = sam_model_registry["vit_h"](checkpoint=checkpoint)
        #sam.to(device="cuda")
        mask_generator = SamAutomaticMaskGenerator(sam)

        #calculate IoU
        totalIoU(data_folder)
