import os
import scipy
import mne
import re

from .base_preprocess import *

def find_subject_mat(path, subject_id, session_id):
    # SEED数据集根据subject_id, session_id获取对应的.mat数据
    files = os.listdir(path)  
    filtered_files = [f for f in files if f.startswith(f"{subject_id}_")]
    filtered_files.sort()

    if session_id <= len(filtered_files):
        selected_file = filtered_files[session_id - 1]  # 注意索引从0开始，所以session_id要减1
    else:
        raise ValueError("session_id not exists in seed_preprocess.py")

    return selected_file
    
class SeedPreprocess(BasePreprocess):
    def __init__(self, args):
        super(SeedPreprocess, self).__init__(args)

    def _load_data(self, path):
        label_path = os.path.join(self.folder, 'label.mat')
        label_mat = scipy.io.loadmat(label_path)['label']
        if self.split_criteria == 'dependent':
            # 对于被试依赖的设置，需要根据yaml中的session_id, subject_id获取对应的mat数据
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject_id'], self.args['session_id']))
            origin_data = scipy.io.loadmat(path)
            data = [value for key, value in origin_data.items() if 'eeg' in key]
            label = [label_mat[0][int(key.split('eeg')[1]) - 1] for key, value in origin_data.items() if 'eeg' in key]
        elif self.split_criteria == 'independent':
            data = []
            label = []
            filtered_files = [file for file in os.listdir(self.folder) if file.split('_')[0].isdigit()]
            sorted_files = sorted(filtered_files, key=lambda x: int(x.split('_')[0])) # 每个被试对应的3个mat会被放置在相邻位置上
            # TODO: 目前是把前6个文件全都读进来了，这样测试的时间短一点，加载45个还是15个文件，需要进一步找参考文献，目前用的是45个文件
            # for i in sorted_files:
            for i in sorted_files[:6]:
                path = os.path.join(self.folder, i) 
                origin_data = scipy.io.loadmat(path)
                for key, value in origin_data.items(): # SEED中每个mat文件都是按照eeg1,eeg2,...,eeg15这样的顺序排列的
                    if 'eeg' in key:
                        data.append(value)
                        label.append(label_mat[0][int(key.split('eeg')[1])-1])
        else:
            raise ValueError(f"{self.args['name']}, {self.args['split_criteria']} should be dependent or independent")  
        return data, label

    def _load_feature(self, data, feature_list):
        label_path = os.path.join(self.folder, 'label.mat')
        label_mat = scipy.io.loadmat(label_path)['label']
        data_dict = {key: [] for key in feature_list}
        label = []
        if self.split_criteria == 'dependent':
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject_id'], self.args['session_id']))
            origin_fea = scipy.io.loadmat(path)
            for i in range(self.args['num_trials']): # 对每个trial的数据进行读取
                for key, value in sorted(origin_fea.items()):
                    if re.findall(r'\d+', key) and int(re.findall(r'\d+', key)[0]) == (i + 1) and re.sub(r'\d+', '', key) in self.args['feature_list']:
                        data_dict[re.sub(r'\d+', '', key)].append(value)
                label.append(label_mat[0][i])
        elif self.split_criteria == 'independent':
            filtered_files = [file for file in os.listdir(self.folder) if file.split('_')[0].isdigit()]
            sorted_files = sorted(filtered_files, key=lambda x: int(x.split('_')[0]))
            # for i in sorted_files: 
            for i in sorted_files[:6]:  # TODO: 目前是把前6个特征文件全都读进来了，这样测试的时间短一点，加载45个还是15个文件，需要进一步找参考文献，目前用的是45个文件
                path = os.path.join(self.folder, i) 
                origin_fea = scipy.io.loadmat(path)
                for i in range(self.args['num_trials']):
                    for key, value in origin_fea.items():
                        if re.findall(r'\d+', key) and int(re.findall(r'\d+', key)[0]) == (i + 1) and re.sub(r'\d+', '', key) in self.args['feature_list']:
                            data_dict[re.sub(r'\d+', '', key)].append(value)
                    label.append(label_mat[0][i])
        else:
             raise ValueError(f"{self.args[self.name]}, {self.args[self.split_criteria]} should be dependent or independent")  

        # for key, value in data_dict.items():
        #     # data_dict[key] = np.concatenate(value, axis=1)
        #     print(len(value))
        #     print(value[0].shape)
        # print(data_dict)
        return data_dict, label

    def _preprocess(self, data):
        montage = mne.channels.read_custom_montage(self.args['location'],coord_frame='head')
        self.ch = self.args['channels']
        preprocess_data = []
        # 为了速度快，这里只跑两个全流程就返回了，仅供测试使用
        for sub_data in data[:2]:
            # step1: 数据处理
            info = mne.create_info(
                ch_names = self.ch,
                ch_types = ['eeg' for _ in range(62)], 
                sfreq = self.args['time_sample'] #采样频率
                ) 
            raw = mne.io.RawArray(sub_data, info) #生成raw
            raw.set_montage(montage)
            # step2: 滤波
            raw.filter(l_freq=self.args['l_freq'], h_freq=self.args['h_freq'],picks='all') # 默认method为FIR，括号内加method：(l_freq=0.1, h_freq=30,method='iir')可修改滤波方法为IIR
            raw.notch_filter(freqs = (self.args['notch_freq']),picks='all')
            
            # step3: 坏导剔除，这一步要加可视化吗？
            raw.load_data()
            raw.interpolate_bads(exclude=self.args['bad_channel'])

            # step4: 重参考
            raw_ref = raw.copy()
            raw_ref.load_data()
            raw_ref.set_eeg_reference(ref_channels='average')

            # step5: 去伪迹
            ica = mne.preprocessing.ICA(n_components=62, 
                                noise_cov=None, 
                                random_state=None, 
                                method='fastica', 
                                fit_params=None, 
                                max_iter='auto', 
                                allow_ref_meg=False, 
                                verbose=True)
            ica.fit(raw_ref)
            ica.exclude = [0, 1] # details on how we picked these are omitted here
            raw_recons = raw_ref.copy()
            raw_recons = ica.apply(raw_recons)

            preprocess_data.append(raw_recons.get_data())
            # print(raw_recons.get_data())
        return preprocess_data

    def _split(self, data, label):
        train_feature_dict={}
        test_feature_dict={}
        train_label=[]
        test_label=[]
        shuffle_index = np.random.permutation(len(data[0])) if self.args['split_shuffle'] else []
        for key, value in data.items():
            train_feature_dict[key], test_feature_dict[key], train_label, test_label = self._split_feature(data[key], label, shuffle=self.args['split_shuffle'], shuffle_index=shuffle_index)
        return train_feature_dict, test_feature_dict, train_label, test_label

    def _split_feature(self, data, label, shuffle=False, shuffle_index=None):
        if self.split_criteria == 'dependent':
            # SEED 数据集被试依赖的划分是把15个trial中9个划分为训练集，6个划分为测试集
            # 参考论文《Investigating Critical Frequency Bands and Channels for EEG-Based Emotion Recognition with Deep Neural Networks》，为了平均数据，我们按照情绪类别的进行划分，积极、消极、中性情绪的前3个trial为训练集，后2个trial为测试集
            if shuffle and shuffle_index: # shuffle data, default False，而且用的同一个shuffle_index,这样才能保证相同的
                data = data[shuffle_index]
                label = label[shuffle_index]
            train_indices = []
            test_indices = []
            for i, num in enumerate(label):
                if label[:i+1].count(num) <= 3:
                    train_indices.append(i)
                else:
                    test_indices.append(i)

            train_label = []
            test_label = []
            train_feature = [data[i] for i in train_indices]
            _train_label = [label[i] for i in train_indices]
            test_feature = [data[i] for i in test_indices]
            _test_label = [label[i] for i in test_indices]
            # 生成对应的标签
            for index, sub_feature in enumerate(train_feature):
                train_label.append(np.repeat(_train_label[index], sub_feature.shape[1]))
            for index, sub_feature in enumerate(test_feature):
                test_label.append(np.repeat(_test_label[index], sub_feature.shape[1]))
            # concat 
            train_feature = np.concatenate(train_feature, axis=1)
            train_label = np.concatenate(train_label, axis=0)
            test_feature = np.concatenate(test_feature, axis=1)
            test_label = np.concatenate(test_label, axis=0)
        elif self.split_criteria == 'independent':
            # TODO: 这块好像太复杂了，得考虑怎么简化一下
            train_feature = [data[i] for i in range(len(data)) if i < (self.args['subject_leave_id'] - 1) * self.args['num_trials']*self.args['num_sessions']  or i >= (self.args['subject_leave_id'])*self.args['num_trials']*self.args['num_sessions']]
            _train_label = [label[i % self.args['num_trials']] for i in range(len(data)) if i < (self.args['subject_leave_id'] - 1) * self.args['num_trials']*self.args['num_sessions']  or i >= (self.args['subject_leave_id'])*self.args['num_trials']*self.args['num_sessions']]
            test_feature = [data[i] for i in range(len(data)) if i >= (self.args['subject_leave_id'] - 1) * self.args['num_trials']*self.args['num_sessions']  and i < self.args['subject_leave_id']*self.args['num_trials']*self.args['num_sessions']]
            _test_label = [label[i % self.args['num_trials']] for i in range(len(data)) if i >= (self.args['subject_leave_id'] - 1) * self.args['num_trials']*self.args['num_sessions']  and i < self.args['subject_leave_id']*self.args['num_trials']*self.args['num_sessions']]
            
            train_label = []
            test_label = []
            for index, sub_feature in enumerate(train_feature):
                train_label.append(np.repeat(_train_label[index], sub_feature.shape[1]))
            for index, sub_feature in enumerate(test_feature):
                test_label.append(np.repeat(_test_label[index], sub_feature.shape[1]))
            train_feature = np.concatenate(train_feature, axis=1)
            train_label = np.concatenate(train_label, axis=0)
            test_feature = np.concatenate(test_feature, axis=1)
            test_label = np.concatenate(test_label, axis=0)
           
        else:
            raise ValueError(f"{self.args[self.name]}, {self.args[self.split_criteria]} should be dependent or independent") 

      
        return train_feature, test_feature, train_label, test_label

        