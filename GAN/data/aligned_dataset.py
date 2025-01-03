import os
from data.base_dataset import BaseDataset, get_params, get_transform
from data.image_folder import make_dataset
import tifffile


class AlignedDataset(BaseDataset):
    """A dataset class for paired image dataset.

    It assumes that the directory '/path/to/data/train' contains image pairs in the form of {A,B}.
    During test time, you need to prepare a directory '/path/to/data/test'.
    """

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)
        self.dir_AB = os.path.join(opt.dataroot, opt.phase)  # get the image directory
        self.AB_paths = sorted(make_dataset(self.dir_AB, opt.max_dataset_size))  # get image paths
        self.val_dir_AB = os.path.join(opt.dataroot, "val")  # get the image directory
        self.val_AB_paths = sorted(make_dataset(self.val_dir_AB, opt.max_dataset_size))  # get image paths

        assert(self.opt.load_size >= self.opt.crop_size)   # crop_size should be smaller than the size of loaded image
        self.input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.output_nc = self.opt.input_nc if self.opt.direction == 'BtoA' else self.opt.output_nc

        # get length of val_data
        self.val_length = len([elm for elm in os.listdir(os.path.join(opt.dataroot, "val")) if elm.split(".")[-1] == "tiff"])  # get the image directory

    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index - - a random integer for data indexing

        Returns a dictionary that contains A, B, A_paths and B_paths
            A (tensor) - - an image in the input domain
            B (tensor) - - its corresponding image in the target domain
            A_paths (str) - - image paths
            B_paths (str) - - image paths (same as A_paths)
        """
        # read a image given a random integer index
        AB_path = self.AB_paths[index]
        AB = tifffile.imread(AB_path)
        mid_index = AB.shape[1] // 2
        A = AB[:, :mid_index]
        B = AB[:, mid_index:]

        # apply the same transform to both A and B
        transform_params = get_params(self.opt, A.shape)
        A_transform = get_transform(self.opt, transform_params, grayscale=(self.input_nc == 1))
        B_transform = get_transform(self.opt, transform_params, grayscale=(self.output_nc == 1))

        A = A_transform(A)
        B = B_transform(B)


        # validation set
        index_val = index % self.val_length
        val_AB_path = self.val_AB_paths[index_val]
        val_AB = tifffile.imread(val_AB_path)
        mid_index = val_AB.shape[1] // 2
        val_A = val_AB[:, :mid_index]
        val_B = val_AB[:, mid_index:]

        # apply the same transform to both val_a and val_B that was applied to A and B
        transform_params = get_params(self.opt, val_A.shape)

        A_transform = get_transform(self.opt, transform_params, grayscale=(self.input_nc == 1))
        B_transform = get_transform(self.opt, transform_params, grayscale=(self.output_nc == 1))
        val_A = A_transform(val_A)
        val_B = B_transform(val_B)

        return {'A': A, 'B': B, 'A_paths': AB_path, 'B_paths': AB_path, 'val_A': val_A, 'val_B': val_B, 'val_A_paths': val_AB_path, 'val_B_paths': val_AB_path}

    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.AB_paths)
