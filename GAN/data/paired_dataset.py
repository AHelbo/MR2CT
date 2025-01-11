import os
from data.base_dataset import BaseDataset, get_params, get_transform
from data.image_folder import make_dataset
import tifffile

class PairedDataset(BaseDataset):
    def __init__(self, opt):
        
        BaseDataset.__init__(self, opt)

        self.A_paths = self.get_paths(opt.phase, 'A', opt)
        self.B_paths = self.get_paths(opt.phase, 'B', opt)
        self.val_A_paths = self.get_paths("val", 'A', opt)
        self.val_B_paths = self.get_paths("val", 'B', opt)

        assert(self.opt.load_size >= self.opt.crop_size)   # crop_size should be smaller than the size of loaded image
        self.input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.output_nc = self.opt.input_nc if self.opt.direction == 'BtoA' else self.opt.output_nc


    def __getitem__(self, index):
        val_index = index % len(self.val_A_paths)
        return {
                'A_paths': self.A_paths[index], 
                'B_paths': self.B_paths[index], 
                'A': self.get_transformed_item(self.A_paths[index], self.input_nc), 
                'B': self.get_transformed_item(self.B_paths[index], self.output_nc), 
                'val_A_paths': self.val_A_paths[val_index], 
                'val_B_paths': self.val_B_paths[val_index],
                'val_A': self.get_transformed_item(self.val_A_paths[val_index], self.input_nc), 
                'val_B': self.get_transformed_item(self.val_B_paths[val_index], self.output_nc), 
                }

    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.A_paths)

    def get_paths(self, phase, subfolder, opt):
        """Helper function to construct directory path and retrieve sorted dataset paths."""
        dir_path = os.path.join(opt.dataroot, phase, subfolder)
        return sorted(make_dataset(dir_path, opt.max_dataset_size))    


    def get_transformed_item(self, path, nc):
        AorB = tifffile.imread(path)
        AorB_shape = AorB.shape[:2]
        transform_params = get_params(self.opt, AorB_shape)
        AorB_transform = get_transform(self.opt, transform_params, grayscale=(nc == 1))
        return AorB_transform(AorB)