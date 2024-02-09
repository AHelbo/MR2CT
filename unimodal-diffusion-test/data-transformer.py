import os
import torchvision
from torchvision import datasets, transforms
from torch.utils.data.dataset import Dataset
from torchvision.datasets.utils import download_url, extract_archive

class GTSRBTrafficSigns(Dataset):
  """ GTSRB data set """

  def __init__(self, train=True, crop_size=28, img_dims=[128,128]): 

    self.img_height  = img_dims[0]  
    self.img_width   = img_dims[1] 
    self.img_height_crop = crop_size  
    self.img_width_crop  = crop_size

    self.train = train
    
    archive = os.path.join(root, filename)

    if self.train:
      self.data_folder = os.path.join(root, 'GTSRB/train')
    else:
      self.data_folder = os.path.join(root, 'GTSRB/test')

    if (not os.path.exists(self.data_folder)) or force_download:
      download_url(url, root, filename)
      extract_archive(archive, root, False)
    else:
      print('Using existing', self.data_folder)

    self.dataset_train = datasets.ImageFolder(self.data_folder)

  def __getitem__(self, index):
      image, label = self.dataset_train.__getitem__(index)
      image = transforms.Resize((self.img_width,self.img_height))(image)
      
      # These transformations just serve as examples
      if self.train:
        image = transforms.RandomPerspective(distortion_scale=2.5)(image)
        image = transforms.RandomAffine((-5,5))(image)
        image = transforms.RandomCrop((self.img_width_crop, self.img_height_crop))(image)
        image = transforms.ColorJitter(0.8, contrast = 0.4)(image)
        if label in [11, 12, 13, 17, 18, 26, 30, 35]:
          image = transforms.RandomHorizontalFlip(p=0.5)(image)
      else:
        image = transforms.CenterCrop((self.img_width_crop, self.img_height_crop))(image)

      image = transforms.ToTensor()(image)

      return image, label

  def __len__(self):
      return self.dataset_train.__len__()
