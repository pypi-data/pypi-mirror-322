import os
import scipy
import mne
import re

from .base_preprocess import *

def find_subject_mat(path):
    files = os.listdir(path)  
    target_file = next((f for f in files if f.startswith(f"DREAMER")), None)  
    assert target_file, f"find_subject_mat(): no proper mat fit DREAMER.mat in {path}"
    return target_file


class DreamerPreprocess(BasePreprocess):
    def __init__(self, args):
        super(DreamerPreprocess, self).__init__(args)

    def _load_data(self, path):
        if self.args['split_criteria'] == 'dependent':
            path = os.path.join(self.folder, find_subject_mat(self.folder))
            origin_data = scipy.io.loadmat(path)
            struct_data = origin_data['DREAMER']['Data'][0,int(self.args['subject_id']) - 1][0,0]
            data = struct_data['EEG'][0,0]['stimuli'][0,0]
            data = [data[i,0] for i in range(data.shape[0])]
            label = struct_data['Score'+self.args['emotion_names'][0]][0,0]
            label = [1 if sub_label >=5 else 0 for sub_label in label]
        elif self.args['split_criteria'] == 'independent':
            pass
        else:
            raise ValueError(f"{self.args[name]}, {self.args[split_criteria]} should be dependent or independent")   
        return data, label

    def _load_feature(self,  data, feature_list):
        pass
    
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
            # 将某个被试的18个trial随机划分为10组，其中8组由2个trial组成，2组由1个trial组成，然后进行十折的留一验证。《DREAMER: A Database for Emotion Recognition Through EEG and ECG Signals From Wireless Low-cost Off-the-Shelf Devices》
            if self.args['split_shuffle']: # default False
                np.random.shuffle(data)
                np.random.shuffle(label)

            # TODO：n折交叉验证还没实现，没想好在哪里实现，感觉整体的架构还是有点问题
            train_feature = np.concatenate(train_feature, axis=1)
            train_label = np.concatenate(train_label, axis=0)
            test_feature = np.concatenate(test_feature, axis=1)
            test_label = np.concatenate(test_label, axis=0)
        elif self.split_criteria == 'independent':
            pass
        else:
            raise ValueError(f"{self.args[name]}, {self.args[split_criteria]} should be dependent or independent")   

        return train_feature, test_feature, train_label, test_label