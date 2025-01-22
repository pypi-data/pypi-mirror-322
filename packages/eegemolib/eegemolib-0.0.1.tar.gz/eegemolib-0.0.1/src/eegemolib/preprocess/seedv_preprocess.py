import os
import scipy
import mne

from .base_preprocess import *
import numpy as np
import pickle


def find_subject_mat(path, subject_id, session_id):
    files = os.listdir(path)  
    target_file = next((f for f in files if f.startswith(f"{subject_id}_")), None)  
    assert target_file, f"find_subject_mat(): no proper npz fit {subject_id}_xxx.npz in {path}"
        
    return target_file

def find_session_label(session_id):
    if session_id == 1:
        return [4,1,3,2,0,4,1,3,2,0,4,1,3,2,0]
    elif session_id == 2:
        return [2,1,3,0,4,4,0,3,2,1,3,4,1,2,0]
    elif session_id == 3:
        return [2,1,3,0,4,4,0,3,2,1,3,4,1,2,0]
    else:
        raise ValueError(f"session_id should be in range in find_session_label()")  
    
class SeedVPreprocess(BasePreprocess):
    def __init__(self, args):
        super(SeedVPreprocess, self).__init__(args)

    def _load_data(self, path):
        if self.args['split_criteria'] == 'dependent':
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject_id'],self.args['session_id']))
            print(path)
            origin_data = np.load(path, allow_pickle=True)
            npy_data = pickle.loads(origin_data['data'])
            npy_label = pickle.loads(origin_data['label'])
            data = [npy_data[key].reshape((-1, 62,5)).transpose(1,0,2).reshape((62,-1)) for key in npy_data]
            label = [npy_label[key] for key in npy_label]
        elif self.args['split_criteria'] == 'independent':
            # 目前是把2个文件(包括3个session的数据)读进来了，这样测试的时间短一点，
            data = []
            label = []
            for i in os.listdir(self.folder)[:2]:
                path = os.path.join(self.folder, i) 
                origin_data = scipy.io.loadmat(path)
                npy_data = pickle.loads(origin_data['data'])
                npy_label = pickle.loads(origin_data['label'])
        else:
            raise ValueError(f"{self.args['name']}, {self.args['split_criteria']} should be dependent or independent")   
        return data, label

    def _load_feature(self, data, feature_list):
        if self.args['split_criteria'] == 'dependent':
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject_id'],self.args['session_id']))
            origin_data = np.load(path, allow_pickle=True)
            npy_data = pickle.loads(origin_data['data'])
            npy_label = pickle.loads(origin_data['label'])
            data = [npy_data[key].reshape((-1, 62,5)).reshape((-1,62*5)) for key in npy_data]
            label = [npy_label[key] for key in npy_label]
        elif self.args['split_criteria'] == 'independent':
            # TODO: 目前是把2个文件(一个文件就包括3个session了)全都读进来了，这样测试的时间短一点，加载45个还是15个文件夹，需要找参考文献，现在加载的是所有session
            data = []
            label = []
            for i in os.listdir(self.folder)[:2]:
                path = os.path.join(self.folder, i) 
                origin_data = np.load(path, allow_pickle=True)
                npy_data = pickle.loads(origin_data['data'])
                npy_label = pickle.loads(origin_data['label'])
                # trial_fea = [npy_data[key].reshape((-1, 62,5)).reshape((-1,62*5)) for key in npy_data]
                # trial_label = [npy_label[key] for key in npy_label]
                for key in npy_data:
                    data.append(npy_data[key].reshape((-1, 62,5)).reshape((-1,62*5)))
                    label.append(npy_label[key])
        else:
            raise ValueError(f"{self.args['name']}, {self.args['split_criteria']} should be dependent or independent")   
        return data, label

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
        if self.split_criteria == 'dependent':
            train_feature = [data[i] for i in range(self.args['num_trials'])]
            test_feature = [data[i + self.args['num_trials']] for i in range(self.args['num_trials']*2)]
            train_label = [label[i] for i in range(self.args['num_trials'])]
            test_label = [label[i + self.args['num_trials']] for i in range(self.args['num_trials']*2)]

            train_feature = np.concatenate(train_feature, axis=0)
            train_label = np.concatenate(train_label, axis=0)
            test_feature = np.concatenate(test_feature, axis=0)
            test_label = np.concatenate(test_label, axis=0)

            print(len(train_feature), len(test_feature),len(train_label), len(test_label))
        elif self.split_criteria == 'independent':
            train_feature = [data[i] for i in range(len(data)) if i < (self.args['subject_leave_id'] - 1) * self.args['num_trials']*self.args['num_sessions']  or i >= (self.args['subject_leave_id'])*self.args['num_trials']*self.args['num_sessions']]
            _train_label = [label[i % self.args['num_trials']] for i in range(len(data)) if i < (self.args['subject_leave_id'] - 1) * self.args['num_trials']*self.args['num_sessions']  or i >= (self.args['subject_leave_id'])*self.args['num_trials']*self.args['num_sessions']]
            test_feature = [data[i] for i in range(len(data)) if i >= (self.args['subject_leave_id'] - 1) * self.args['num_trials']*self.args['num_sessions']  and i < self.args['subject_leave_id']*self.args['num_trials']*self.args['num_sessions']]
            _test_label = [label[i % self.args['num_trials']] for i in range(len(data)) if i >= (self.args['subject_leave_id'] - 1) * self.args['num_trials']*self.args['num_sessions']  and i < self.args['subject_leave_id']*self.args['num_trials']*self.args['num_sessions']]
            
            train_label = _train_label
            test_label = _test_label

            train_feature = np.concatenate(train_feature, axis=0)
            train_label = np.concatenate(train_label, axis=0)
            test_feature = np.concatenate(test_feature, axis=0)
            test_label = np.concatenate(test_label, axis=0)
        else:
            raise ValueError(f"{self.args[name]}, {self.args[split_criteria]} should be dependent or independent")  
        return train_feature, test_feature, train_label, test_label

