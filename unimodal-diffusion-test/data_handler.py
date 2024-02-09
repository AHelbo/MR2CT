import os
import torchvision
from torchvision import datasets, transforms
from torch.utils.data.dataset import Dataset
from torchvision.datasets.utils import download_url, extract_archive

class DataHandler(Dataset):
  """ GTSRB data set """

  def __init__(self, crop_dims=[220,220], img_dims=[256,256], transform = False): 

    self.img_height  = img_dims[0]  
    self.img_width   = img_dims[1] 
    self.img_height_crop = crop_dims[0]  
    self.img_width_crop  = crop_dims[1]

    self.transform = transform

    # needs to be different I guess, too tired though
    archive = os.path.join("/Users/andershelbo/Dropbox/Documents/Datalogi/Bachelor/MRI2CT-DATA/stanford_cars/cars_train")

    self.dataset = datasets.ImageFolder(archive)


  def __getitem__(self, index):
      image, label = self.dataset.__getitem__(index)
      
      # These transformations just serve as examples
      if self.transform:
        image = transforms.RandomCrop((self.img_width_crop, self.img_height_crop))(image)
        image = transforms.RandomAffine(degrees=10,translate=10)

      image = transforms.Resize((self.img_width,self.img_height))(image)

      image = transforms.ToTensor()(image)

      return image, label


  def __len__(self):
      return self.dataset.__len__()


if __name__ == '__main__':

  handler = DataHandler()
  print(len(handler))
  print(handler.__getitem__(0))
