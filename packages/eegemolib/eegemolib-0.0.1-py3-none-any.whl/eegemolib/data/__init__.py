import importlib
import torch.utils.data

from data.base_dataset import BaseDataset

def find_dataset_using_name(dataset_name: str):
    dataset_filename = "data." + dataset_name.lower() + "_dataset"
    datasetlib = importlib.import_module(dataset_filename)
    dataset = None
    for name, module in datasetlib.__dict__.items():
        if name.lower() == (dataset_name.lower()+'dataset') and issubclass(module, BaseDataset):
            dataset = module

    if dataset is None:
        raise NotImplementedError(f"In {dataset_filename}.py, there should be a subclass of BaseDataset with class name that matches {dataset_name + 'dataset'} in lowercase.")

    return dataset

def create_dataset(args, test=False):
    """
    Create dataset loader with dataset name
    """
    data_loader = CustomDatasetDataLoader(args, test)
    dataset = data_loader.load_data()
    return dataset

class CustomDatasetDataLoader():
    """Wrapper class of Dataset class that performs multi-threaded data loading"""

    def __init__(self, args, test=False):
        """Initialize this class

        Step 1: create a dataset instance given the name [dataset_mode]
        Step 2: create a multi-threaded data loader.
        """
        self.args = args
        self.test = test
        dataset_class = find_dataset_using_name(args['name'])
        if test:
            self.dataset = dataset_class(args, self.test)
        else:
            self.dataset = dataset_class(args)
        print(f"dataloader on dataset {str(self.dataset)} was created")
        shuffle = args['mode'] == 'train'
        if self.test:
            self.dataloader = torch.utils.data.DataLoader(
                self.dataset,
                batch_size=1,
                shuffle=shuffle)

        else:
            self.dataloader = torch.utils.data.DataLoader(
                self.dataset,
                batch_size=args['batch_size'],
                shuffle=shuffle,
                num_workers=8)

    def load_data(self):
        return self

    def __len__(self):
        """Return the number of data in the dataset"""
        return len(self.dataset)

    def __iter__(self):
        """Return a batch of data"""
        if self.test:
            for i, data in enumerate(self.dataloader):
                yield data
        else:
            for i, data in enumerate(self.dataloader):
                if i * self.args['batch_size'] >= len(self.dataloader):
                    break
                yield data