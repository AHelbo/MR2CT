import sys
from skimage.metrics import mean_squared_error
import os
from PIL import Image
import numpy as np

def generate_image_list(path):
    return [os.path.join(path,elm) for elm in os.listdir(path) if not elm == ".DS_Store"]
    
def compare_lists(listA, listB):
    listA = sorted([elm.split("/")[-1].split("_")[0] for elm in listA])
    listB = sorted([elm.split("/")[-1].split("_")[0] for elm in listB])

    if (listA != listB):
        set_A = set(listA)
        set_B = set(listB)
        diff = set_A - set_B
        print(diff)
        raise Exception(f"images are not the same in path A and B")

def calculate_SIMOS(listA, listB):

    listA = sorted(listA)
    listB = sorted(listB)
    compare_lists(listA, listB)

    acc = 0.0
    count = 0

    for (currA, nextA), (currB, nextB) in zip(zip(listA[:-1],listA[1:]),zip(listB[:-1],listB[1:])):
        
        try:
            #if images are not adjacent (ie same pid and neighboring slicenumber) do nothing
            # check if same pid
            curr_pid = currA.split("/")[1].split("-")[0]
            next_pid = nextA.split("/")[1].split("-")[0]
            if (curr_pid != next_pid):
                continue
            
            # check if adjacent slice number
            curr_slice = int(currA.split("/")[-1].split("-")[1].split("_")[0])
            next_slice = int(nextA.split("/")[-1].split("-")[1].split("_")[0])
            if (next_slice-curr_slice != 1):
                continue

            currA_im = np.array(Image.open(currA))
            nextA_im = np.array(Image.open(nextA))
            diffA = mean_squared_error(currA_im, nextA_im)

            currB_im = np.array(Image.open(currB))
            nextB_im = np.array(Image.open(nextB))
            diffB = mean_squared_error(currB_im, nextB_im)
            
            acc += abs(diffA-diffB)
            count += 1
        except:
            pass

    if (count == 0):
        return 0

    return acc/count

def write_to_file(output_file_path, epoch, SEC):
    with open(output_file_path, "a") as file:
        file.write(f"EPOCH {epoch} SIMOS {SEC}\n")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 calculate_SIMOS.py <pathA> <pathB> <epoch> <path to output file>")

    else:
        print("Calculating SIMOS")

        # create dict of patients and their slices withing this folder. Slices that are not i and i+1 should be omitted
        real_B = sys.argv[1]
        real_list = generate_image_list(real_B)

        # create dict of patients and their slices withing this folder. Slices that are not i and i+1 should be omitted
        fake_B = sys.argv[2]
        fake_list = generate_image_list(fake_B)

        # compare real_list and fake_list, everything must line up.
        compare_lists(real_list,fake_list)

        # iterating through both lists, calculate the mean absolute difference bewteen the mse between each slice i and i+1
        SIMOS = calculate_SIMOS(real_list, fake_list)

        # write the result as SIMOS (slice-wise difference comparison) to file
        epoch = sys.argv[3]
        path_to_output_file = sys.argv[4]
        write_to_file(path_to_output_file, epoch, SIMOS)

        print(" Done")
