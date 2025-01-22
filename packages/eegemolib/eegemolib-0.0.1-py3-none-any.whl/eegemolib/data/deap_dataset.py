import os
import re
import errno
import tqdm
import numpy as np
import torch.nn.functional as F
from scipy.io import loadmat

from data.base_dataset import BaseDataset, get_transform
from utils.utils import *

# define the DEAP dataset class
class DEAPDataset(BaseDataset):
    def __init__(self, args, test=False):
        super(DEAPDataset, self).__init__(args)

        self.args = args
        self.win_len = args['win_length']
        self.num_classes = args['num_classes']
        self.root = self.args['save_path']
        self.test = test
        print(self.root)
        if (check_cache(self.root)): # 如果有已经生成好的cache数据，直接读入
            self.data, self.label = load_cache(self.root)
            self.test_data, self.test_label = load_cache(self.root.replace('train', 'test'))

        self.len = self.data.shape[1] // self.args['win_length']
        self.test_len = self.test_data.shape[1]

    def _map_eeg2label(self, data, label_mat):
        # DEAP/data_preprocessed_matlab下的文件是将data和label分开存放的，已规整（data只读取前32维EEG相关）
        eeg = np.array(data['data'][:, 0:32, :], dtype=float)
        # label = np.array(data['labels'][:, self.label_dimension], dtype=int)
        # 以valence维度为例， 将1-9归为0-1二分类
        label = data['labels'][:, self.label_dimension]
        label = np.array(label > 5.0, dtype=int) # valence, arousal, dominance, liking. change from double to int
        
        return eeg, label

    def __getitem__(self, index):
        # TODO：将特征转换为二维的图像，可以合并到transforms里面，也可以合并到特征提取里面，没考虑好放哪里，先单独实现一下
        mapping = np.array([[0,3],[1,3],[2,0],[2,2],[3,3],[3,1],[4,0],[4,2],[5,3],[5,1],[6,0],[6,2],[6,4],[7,4],[8,3],[8,4],[8,5],[7,5],[6,6],[6,8],[5,7],[5,5],[4,6],[4,8],[3,7],[3,5],[2,6],[2,8],[1,5],[0,5]])
        batch_data = np.zeros((9, 9, 4))
        if self.test:
            clip_data = self.test_data[index: index+1, :]
            batch_label = np.eye(N=1, M=self.num_classes, k=self.test_label[index][0]+ 1).squeeze()
        else:
            clip_data = self.data[index: index+1, :]
            batch_label = np.eye(N=1, M=self.num_classes, k=self.label[index][0]+ 1).squeeze()
        for channel in range(30):
            batch_data[mapping[channel, 0], mapping[channel, 1],:] = clip_data[:, channel*4:(channel+1) * 4]
        # TODO: do not transform label to one-hot encoding
        # batch_label = self.label[index * self.win_len]
        # transform label to one-hot encoding
       
        
        transforms = get_transform()
        batch_data_transform = transforms(batch_data)
        
        return {'data': batch_data_transform, 'label': batch_label}

    def __len__(self):
        return self.len

    def __str__(self):
        return "DEAP"

