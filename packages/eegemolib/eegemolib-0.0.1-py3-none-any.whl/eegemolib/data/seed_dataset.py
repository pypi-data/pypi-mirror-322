import os
import re
import errno
import tqdm
import numpy as np
from scipy.io import loadmat
import torch.nn.functional as F

from data.base_dataset import BaseDataset, get_transform
from utils.utils import *

# define the SEED dataset class
class SeedDataset(BaseDataset):
    def __init__(self, args, test=False):
        self.args = args
        # dataset own setting
        # self.root = args['data']
        # self.split_criterion = args['split_criteria']
        # self.subject = args['subject']
        # self.split_proportion = args['split_proportion']
        self.win_len = args['win_length']
        self.num_classes = args['num_classes']
        self.test = test

        # assert(check_dir(self.root)),f"{self.root} not exist while building SEED dataset"
        # assert self.subject in range(self.dataset_numSubjects + 1) if self.split_criterion == 'dependent' else True, \
        #     "subject ID should be setted if using subject_dependent split criterion"
        self.root = self.args['save_path']
        if self.test == False:
            self.data, self.label = load_cache(os.path.join(self.root, 'train.cache'))
        else:
            self.data, self.label = load_cache(os.path.join(self.root, 'test.cache'))
            
        # else:
        #     self.data, self.label = self.split_dependent() if self.split_criterion == 'dependent' \
        #         else self.split_independent()
        # print(self.data.shape, self.test_data.shape)
        self.len = self.data.shape[0] // self.args['win_length']

    # def split_dependent(self):
    #     print("load SEED dataset using subject dependent setting")
    #     # 先把第10个人的demo为例做测试,后面要根据subject寻找
    #     mat = loadmat(os.path.join(self.root, '10_20131130.mat')) 
    #     label = loadmat(os.path.join(self.root, 'label.mat'))
    #     label = label['label']
    #     data, label = self._map_eeg2label(mat, label)
        
    #     # downsample, and split train set, val set, test set, save in cache
    #     # TODO: 这里也有两种subject dependent的方式，一种是shuffle以后划分，一种是一个trail前面和后面的划分
    #     train_data, train_label = [], []
    #     test_data, test_label = [], []
    #     for trial in range(len(data)):
    #         data[trial] = data[trial][:, ::self.args['down_sample']]
    #         label[trial] = label[trial][::self.args['down_sample']]

    #         timestamps = len(data[trial][0])
    #         train_data.append(data[trial][:,:int(timestamps * self.args['split_proportion'])])
    #         train_label.append(label[trial][:int(timestamps * self.args['split_proportion'])])
    #         test_data.append(data[trial][:,int(timestamps * self.args['split_proportion']):])
    #         test_label.append(label[trial][int(timestamps * self.args['split_proportion']):])

    #     train_data = np.hstack(train_data)
    #     train_label = np.hstack(train_label)
    #     test_data = np.hstack(test_data)
    #     test_label = np.hstack(test_label)

    #     assert train_data.shape[1] == train_label.shape[0] and \
    #         test_data.shape[1] == test_label.shape[0], " data and label not match"

    #     save_cache(os.path.join(self.root, 'train.cache'), {'data': train_data, 'label':train_label})
    #     save_cache(os.path.join(self.root, 'test.cache'), {'data': test_data, 'label':test_label})
    #     return train_data, train_label
       

    # def split_independent(self):
    #     print("load SEED dataset using subject independent setting")
    #     pass

    # def _map_eeg2label(self, data, label_mat):
    #     eeg = []
    #     label = []
    #     for key, value in data.items():
    #         if 'eeg' not in key: # 没有EEG标识的直接跳过,SEED中的EEG数据存储在xxx_eeg{trial}中
    #             continue

    #         trial_data = data[key]
    #         trial_label = [label_mat[0][int(key.split('eeg')[-1]) - 1]] * len(trial_data[0])
    #         eeg.append(np.array(trial_data))
    #         label.append(np.array(trial_label))
    #     return eeg, label

    def __getitem__(self, index):
        batch_data = self.data[index * self.win_len : (index + 1) * self.win_len]
        # transform label to one-hot encoding
        labels = self.label[index * self.win_len: (index + 1) * self.win_len] + 1
        # print("labels:",labels)
        # 创建 one-hot 编码矩阵
        batch_label = np.eye(self.num_classes)[labels].squeeze()

        transforms = get_transform()
        batch_data_transform = transforms(batch_data)
        
        return {'data': batch_data_transform, 'label': batch_label}

    def __len__(self):
        return self.len

    def __str__(self):
        return "SEED"

