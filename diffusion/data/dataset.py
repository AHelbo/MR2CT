import torch.utils.data as data
from torchvision import transforms
from PIL import Image
import os
import torch
import numpy as np

from tifffile import imread, imwrite

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
    'tiff'
]

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)

def make_dataset(dir):
    if os.path.isfile(dir):
        images = [i for i in np.genfromtxt(dir, dtype=np.str, encoding='utf-8')]
    else:
        images = []
        assert os.path.isdir(dir), f'{dir} is not a valid directory {os.path.isdir(dir)}'
        for root, _, fnames in sorted(os.walk(dir)):
            for fname in sorted(fnames):
                if is_image_file(fname):
                    path = os.path.join(root, fname)
                    images.append(path)
    return images


def pil_loader(path):
    return imread(path)


def get_conditional_filenames(flist):
    unique_filenames_set = {elm.split("/")[-1] for elm in flist}

    unique_filenames_list = list(unique_filenames_set)

    return unique_filenames_list


class MR2CTDataset(data.Dataset):
    def __init__(self, data_root, data_flist, data_len=-1, image_size=[256, 256], loader=pil_loader):

        self.data_root = data_root
        flist = make_dataset(data_flist)
        if data_len > 0:
            self.flist = flist[:int(data_len)]
        else:
            self.flist = flist

        # To avoid duplicates run this function. It does change the format of flist contents, beware..
        self.flist = get_conditional_filenames(flist)

        self.tfs_single = transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize((image_size[0], image_size[1])),
                #transforms.Grayscale(num_output_channels=1),
                transforms.Normalize(mean=[0.5], std=[0.5])
        ])

        self.tfs_triple = transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize((image_size[0], image_size[1])),
                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

        self.loader = loader
        self.image_size = image_size

    def __getitem__(self, index):
        ret = {}
        file_name = str(self.flist[index])
        
        # the ground is always a single layer
        gt_img = self.tfs_single(self.loader('{}/{}/{}'.format(self.data_root, 'B', file_name)))

        if (self.in_channel == 2): # grayscale gt + grayscale cond = 2 channels
            cond_image = self.tfs_single(self.loader('{}/{}/{}'.format(self.data_root, 'A', file_name)))
        elif (self.in_channel == 4): # grayscale gt + rgb cond = 4 channels
            cond_image = self.tfs_triple(self.loader('{}/{}/{}'.format(self.data_root, 'A', file_name)))
        else:
            raise Exception("When using MR2CTDataset set_in_channel must be called before sampling to set number of channels in cond img")

        ret['gt_image'] = gt_img
        ret['cond_image'] = cond_image
        ret['path'] = file_name
        return ret

    def __len__(self):
        return len(self.flist)
    
    def set_in_channel(self, nc):
        if (nc != 2 and nc != 4):
            raise Exception("MR2CTDataset only supports 2 or 4 channels in output")
        self.in_channel = nc



