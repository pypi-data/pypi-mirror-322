import os
import scipy
import numpy as np
import mne

from .base_preprocess import BasePreprocess

def find_subject_mat(path, subject): 
    files = os.listdir(path)  
    target_file = next((f for f in files if f.startswith("s%02d" % subject)), None)  
    assert target_file, "find_subject_mat(): no proper mat fit s%02d.mat in %s" % (subject, path)
        
    return target_file
    
class DeapPreprocess(BasePreprocess):
    def __init__(self, args):
        super(DeapPreprocess, self).__init__(args)
        label_list = ['valence', 'arousal', 'dominance', 'liking']
        self.label_dimension = label_list.index(args['emotion_names'][0].lower())

    def _load_data(self, path):
        if self.args['split_criteria'] == 'dependent':
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject_id']))
            origin_data = scipy.io.loadmat(path)
            data = np.array(origin_data['data'][:, 0:32, :], dtype=float)
            
            label = origin_data['labels'][:, self.label_dimension]
            label = np.array(label > 5.0, dtype=int)
        elif self.args['split_criteria'] == 'independent':
            # TODO: deap 数据集的independent设置还没仔细看文献
            data = []
            label = []
            for i in os.listdir(self.folder)[:5]:
                if not i.endswith(".mat"): 
                    continue

                path = os.path.join(self.folder, i) 
                origin_data = scipy.io.loadmat(path)
                subData = np.array(origin_data['data'][:, 0:32, :], dtype=float)
                # subLabel = np.array(data['labels'][:, self.label_dimension], dtype=int)
                subLabel = origin_data['labels'][:, self.label_dimension]
                subLabel = np.array(subLabel > 5.0, dtype=int)
                data.extend(subData.tolist())
                label.extend(subLabel.tolist())
        else:
            raise ValueError(f"{self.args.name}, {self.args.split_criteria} should be dependent or independent")   
        return np.array(data), np.array(label)

    def _load_feature(self, data):
        # TODO: load feature from deap dataset
        return

    def _preprocess(self, data):
        montage = mne.channels.read_custom_montage(self.args['location'],coord_frame='head')
        self.ch = self.args['channels']
        preprocess_data = []
        # 为了速度快，这里只跑两个全流程就返回了，仅供测试使用
        for sub_data in [data]:
            # step1: 数据处理
            info = mne.create_info(
                ch_names = self.ch,
                ch_types = ['eeg' for _ in range(32)], 
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
            ica = mne.preprocessing.ICA(n_components=32, 
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
            train_feature_dict[key], test_feature_dict[key], train_label, test_label = self._split_feature(data[key], label)
        return train_feature_dict, test_feature_dict, train_label, test_label

    def _split_feature(self, origin_data, origin_label):
        data = []
        label = []
        for index, sub_data in enumerate(origin_data):
            # move baseline
            sub_base_data = np.mean(sub_data[:, :3, :], axis=1, keepdims=True)
            trial_data = sub_data[:, 3:, :]
            print(trial_data.shape, sub_base_data.shape)
            data.append(trial_data - sub_base_data)
            # add label
            label.append(np.repeat(origin_label[index], data[index].shape[1]))
    
        data = np.array(data).transpose(1,0,2,3).reshape(32, -1, 4)
        label = np.concatenate(label).reshape(-1, 1)
        print(data.shape)
        print(label.shape)
        len_data = data.shape[1]
        self.split_proportion = self.args['split_proportion']
        # shuffle
        shuffle_index = np.random.permutation(len_data) 
        data = data[:, shuffle_index, :]
        label = label[shuffle_index, :]

        train_feature = data[:, :int(len_data * self.split_proportion),:]
        test_feature = data[:,int(len_data * self.split_proportion):,:]
        train_label = label[:int(len_data * self.split_proportion),:]
        test_label = label[int(len_data * self.split_proportion):,:]
        return train_feature, test_feature, train_label, test_label