import torch.utils.data as data
from abc import ABC, abstractmethod
import torchvision.transforms as transforms

class BaseDataset(data.Dataset, ABC):
    """
    This class is an abstract base class (ABC) for datasets.


    To create a subclass, you need to implement the following four functions:
    -- <__init__>:                      initialize the class, first call BaseDataset.__init__(self, opt).
    -- <__len__>:                       return the size of dataset.
    -- <__getitem__>:                   get a data point.
    -- <modify_commandline_options>:    (optionally) add dataset-specific options and set default options.
    """

    def __init__(self, args):
        """Initialize the class; save the options in the class

        Parameters:
            data: dataset path
            mode: train / test 
        """
        self.args = args

    # @abstractmethod
    # def split_independent(self):
    #     pass
        
    # @abstractmethod
    # def split_dependent(self):
    #     pass

    @abstractmethod
    def __len__(self):
        """Return the total number of images in the dataset."""
        return 0

    @abstractmethod
    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index - - a random integer for data indexing

        Returns:
            a dictionary of data with their names. It ususally contains the data itself and its metadata information.
        """
        pass

    @abstractmethod
    def __str__(self):  
        """ Return the name of current dataset"""
        pass

def get_transform():
    # TODO: add other transform
    transform_list = []

    transform_list.append(transforms.ToTensor())

    return transforms.Compose(transform_list)