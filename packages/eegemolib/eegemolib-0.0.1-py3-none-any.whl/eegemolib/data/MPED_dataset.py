import os
import re
import errno
import tqdm
import numpy as np
import torch.nn.functional as F
from scipy.io import loadmat

from data.base_dataset import BaseDataset, get_transform
from utils.utils import *

LENGTH = 120000

# define the DEAP dataset class
class MPED(BaseDataset):
    def __init__(self, args):
        super(MPED, self).__init__(args)

        self.args = args
        # dataset own setting
        # self.split_criterion = args['split_criteria']
        # self.subject = args['subject_id']
        # self.split_proportion = args['split_proportion']
        self.win_len = args['win_length']
        self.num_classes = args['numClasses']
        
        self.subroots = [subdir for subdir in os.listdir(self.args['folder']) if os.path.isdir(os.path.join(self.args['folder'], subdir))]
        self.labelMacro = loadmat(os.path.join(self.args['folder'], 'raw_EEG_Label.mat'))['eeg_label']
        # assert self.subject in range(self.dataset_numSubjects + 1) if self.split_criterion == 'dependent' else True, \
        #     "subject ID should be setted if using subject_dependent split criterion"
        self.root = self.args['save_path']
        print(self.root)self.data, self.label = self.split_dependent() if self.split_criterion == 'dependent' \
        #         else self.split_independent()
        # 
 
        self.len = self.data.shape[1] // self.args['win_length']

    # def split_dependent(self):
    #     print("load MPED dataset using subject dependent setting")
    #     # 先把第1个人的demo为例做测试,后面要根据subject寻找
    #     currentSub = self.subroots[0]
    #     dir = os.path.join(self.args['folder'], currentSub)
    #     mat_1 = loadmat(os.path.join(dir, f'{currentSub}_d.mat')) # {'__header__': b'MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: Tue Feb 06 15:42:29 2018', '__version__': '1.0', '__globals__': [], 'raw_eeg1': array(xxx)}
    #     mat_2 = loadmat(os.path.join(dir, f'{currentSub}_dd.mat')) 

    #     data, label = self._map_eeg2label(mat_1, mat_2)
    #     print('-*-[After map]' * 10, data.shape, label.shape)
        
    #     # downsample, and split train set, val set, test set, save in cache
    #     # TODO: 这里也有两种subject dependent的方式，一种是shuffle以后划分，一种是一个trail前面和后面的划分
    #     train_data, train_label = [], []
    #     test_data, test_label = [], []
    #     for trial in range(len(data)):
    #         data_t = data[trial][:, ::self.args['down_sample']]
    #         label_t = label[trial][::self.args['down_sample']]

    #         timestamps = data_t.shape[-1]
    #         train_data.append(data_t[:,:int(timestamps * self.args['split_proportion'])])
    #         train_label.append(label_t[:int(timestamps * self.args['split_proportion'])])
    #         test_data.append(data_t[:,int(timestamps * self.args['split_proportion']):])
    #         test_label.append(label_t[int(timestamps * self.args['split_proportion']):])

    #     train_data = np.hstack(train_data)
    #     train_label = np.hstack(train_label)
    #     test_data = np.hstack(test_data)
    #     test_label = np.hstack(test_label)
    #     print('-*- [After stack]', train_label.shape)

    #     assert train_data.shape[1] == train_label.shape[0] and \
    #         test_data.shape[1] == test_label.shape[0], " data and label not match"

    #     return train_data, train_label
       

    # def split_independent(self):
    #     print("load MPED dataset using subject independent setting")
    #     pass

    def _map_eeg2label(self, data, label_mat): # 'data' = mat_1, 'label_mat' = mat_2
        del data['__header__']
        del data['__version__']
        del data['__globals__']
        del label_mat['__header__']
        del label_mat['__version__']
        del label_mat['__globals__']
        eeg = []
        for k, v in data.items():
            eeg.append(v[:, v.shape[1]-LENGTH:])
        for k, v in label_mat.items():
            eeg.append(v[:, v.shape[1]-LENGTH:])

        label = []
        for ll in np.squeeze(self.labelMacro).tolist():
            label.append([ll] * LENGTH)
        
        return np.array(eeg, dtype=np.float16), np.array(label, dtype=np.uint8)

    def __getitem__(self, index):
        batch_data = self.data[:, index * self.win_len : (index + 1) * self.win_len]
        # TODO: do not transform label to one-hot encoding
        # batch_label = self.label[index * self.win_len]
        # transform label to one-hot encoding
        batch_label = np.eye(N=1, M=self.num_classes, k=self.label[index * self.win_len] + 1).squeeze()
        
        transforms = get_transform()
        batch_data_transform = transforms(batch_data)
        
        return {'data': batch_data_transform, 'label': batch_label}

    def __len__(self):
        return self.len

    def __str__(self):
        return "MPED"

