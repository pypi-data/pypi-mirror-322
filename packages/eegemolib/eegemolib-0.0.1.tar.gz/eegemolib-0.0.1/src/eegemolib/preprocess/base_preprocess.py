import mne
import numpy as np
import csv
import os
import scipy.io
from features import *
import importlib  
from utils.utils import save_cache
from abc import ABC, abstractmethod
import preprocess.feature_selection


class BasePreprocess(ABC):
    """
    basic class of preprocess, implement below functions freely
    -- <_load_data>:                      load data 根据路径加载EEG数据
    -- <_load_feature>:                   load features 根据路径加载EEG特征
    -- <_preprocess>:                     preprocess data 预处理流程
    -- <_feature_compute>:                compute features 根据compute_fea_list计算特征
    -- <_feature_selection>:              select features 特征选择
    -- <_split>:                          split train set and test set 划分训练集和测试集
    一般的流程是两条：
    （1）load_data -> preprocess -> feature_compute -> feature_selection -> split （使用EEG数据）
    （2）load_feature -> feature_selection -> split （使用EEG特征）

    目前这里都用的_load_data()而不是__load_data()，感觉不改也行
    """
    def __init__(self, args):
        self.args = args
        self.folder = self.args['folder']
        self.save_path = self.args['save_path']
        self.feature_load = self.args['features']
        self.preprocess = self.args['preprocess']
        self.split_criteria = self.args['split_criteria']
        self.compute_feature = self.args['compute_fea']
        self.feature_selection = self.args['select_fea']
        
    def generate(self): 
        # main loop of preprocessing input data, including load data, prerpocess data, feature extraction, feature selection and split data
        # check cache
        if os.path.exists(os.path.join(self.save_path, 'train.cache')) and os.path.exists(os.path.join(self.save_path, 'test.cache')):
            print('[Warning]: The current path already contains cached train and test data, will use them directly for training. If you wish to preprocess the raw data again, please select an empty folder.')
            return 

        # step1: load data according to self.folder
        if self.feature_load:
            self.data, self.label = self._load_feature(self.folder, self.args['feature_list'])
        else:
            self.data, self.label = self._load_data(self.folder)
        # step2: preprocess data
        if (self.preprocess):
            self.data = self._preprocess(self.data)
        else:
            print("[Warning]: skip preprocess")
        #  step3: extract feature
        if (self.compute_feature):
            self.feature = self._feature_compute(self.data)
            print(len(self.feature))
            # print(self.feature['de'].shape)
        else:
            self.feature = self.data
            print("[Warning]: skip feature compute")
        
        # step4: split train set and test set
        # print(self._split(self.feature, self.label))
        self.train_feature, self.test_feature, self.train_label, self.test_label = self._reshape_feature(*self._split(self.feature, self.label))
       
        # step5: feature slection 
        if (self.feature_selection):
            self.train_feature, self.train_label, self.test_feature, self.test_label = self._feature_selection(self.train_feature, self.test_feature, self.train_label, self.test_label, self.args['select_method'], self.args['select_features'])
        else:
            print("[Warning]: skip feature selection")
        print(f"after preprocess, get train length: {len(self.train_feature)}, label length: {len(self.train_label)}" )
        print(self.train_feature.shape, self.train_label.shape, self.test_feature.shape, self.test_label.shape)
        
        # step6: adjust cache save path and format
        save_cache(os.path.join(self.args['save_path'], 'train.cache'), {'data': self.train_feature, 'label': self.train_label})
        save_cache(os.path.join(self.args['save_path'], 'test.cache'), {'data': self.test_feature, 'label': self.test_label})
        
    @abstractmethod
    def _load_data(self, path): 
        # for each dataset, should implement its own load data method
        pass

    @abstractmethod
    def _load_feature(self, path, feature_list):
        # for each dataset, should implement its own load feature method
        pass

    @abstractmethod 
    def _preprocess(self, data):
        pass
        
    def _feature_compute(self, data):
        print(f"features compute list: {self.args['compute_fea_list']}")
        feature = {}
        # for sub_data in data: # 对每一个trial都进行特征计算
        #     sub_feature = []
        #     for feature_name in self.args['compute_fea_list']:
        #         module = importlib.import_module(f"preprocess.features")  
        #         method = getattr(module, feature_name)
        #         sub_feature.append(method(sub_data, self.args))
        #     sub_feature = np.concatenate(sub_feature, axis=2)  
        #     feature.append(sub_feature)
        for feature_name in self.args['compute_fea_list']: # 在每一个特征下对每一个trial进行计算
            sub_feature = []
            module = importlib.import_module(f"preprocess.features")  
            method = getattr(module, feature_name)
            for sub_data in data:
                sub_feature.append(method(sub_data, self.args))
            # sub_feature = np.array(sub_feature)
            feature[feature_name] = sub_feature
        return feature
            
    def _feature_selection(self, train_feature, test_feature, train_label, test_label, method, num_features):
        # feature selection method in preprocess.feature_selection.py
        print(f"features selection method: {self.args['select_method']}")
        method = getattr(preprocess.feature_selection, 'feature_' + str(method))
        if train_feature.ndim == 3:
            train_samples = train_feature.shape[1]
            test_samples = test_feature.shape[1]
            train_feature = np.transpose(train_feature, axes=(1,0,2)).reshape(train_samples, -1)
            test_feature = np.transpose(test_feature, axes=(1,0,2)).reshape(test_samples, -1)
        # print(train_feature.shape, test_feature.shape)
        train_feature, train_label, test_feature, test_label = method(train_feature, train_label, test_feature, test_label, num_features)
        return train_feature, train_label, test_feature, test_label
    
    def _reshape_feature(self, train_feature_dict, test_feature_dict, train_label, test_label):
        train_feature = []
        test_feature = []
        for key, value in train_feature_dict.items():
            train_samples = train_feature_dict[key].shape[1]
            train_feature.append(np.transpose(train_feature_dict[key], axes=(1,0,2)).reshape(train_samples, -1))
        train_feature = np.concatenate(train_feature, axis=0)
        for key, value in test_feature_dict.items():
            test_samples = test_feature_dict[key].shape[1]
            test_feature.append(np.transpose(test_feature_dict[key], axes=(1,0,2)).reshape(test_samples, -1))
        test_feature = np.concatenate(test_feature, axis=0)

        # normalize 
        row_min = train_feature.min(axis=1).reshape(-1, 1)
        row_max = train_feature.max(axis=1).reshape(-1, 1)
        train_feature = (train_feature - row_min) / (row_max - row_min)
        row_min = test_feature.min(axis=1).reshape(-1, 1)
        row_max = test_feature.max(axis=1).reshape(-1, 1)
        test_feature = (test_feature - row_min) / (row_max - row_min)
        return train_feature, test_feature, train_label, test_label

           
            
    def _split(self, data, origin_label):
        # TODO: shuffle

        # balance the len of label and data
        label = []
        for index, sub_data in enumerate(data):
            label.append(np.repeat(origin_label[index], sub_data.shape[1]))
            # print(sub_data.shape)

        # split train set and test set
        len_data = len(data)
        self.split_proportion = self.args['split_prop']
        train_feature = np.concatenate(data[0: int(len_data * 0.8)], axis=1)
        test_feature = np.concatenate(data[int(len_data * 0.8):], axis=1)
        print(f"train feature shape: {train_feature.shape}, test_feature shape: {test_feature.shape}")
        train_label = np.concatenate(label[0: int(len_data * 0.8)], axis=0)
        test_label = np.concatenate(label[int(len_data * 0.8):], axis=0)
        print(f"train label shape: {train_label.shape}, test_label shape: {test_label.shape}")
        return train_feature, test_feature, train_label, test_label
    
    def _download(self):
        print(f"please visit {self.args['url']} for dataset")
        
    def __str__(self):
        print(f"{self.args['name']} dataset, more details please refer to {self.args['url']}")

