import os
import scipy
import numpy as np
import mne

from .base_preprocess import *

def find_subject_mat(path, subject): # TODO 目前是随机找了一个被试的mat进行读取，但每一个被试其实有三个mat可以用作训练的
    files = os.listdir(path)  
    target_file = next((f for f in files if f.startswith("sub%d" % subject)), None)  
    assert target_file, "find_subject_mat(): no proper mat fit s%d.mat in %s" % (subject, path)
        
    return target_file
    
class CasPreprocess(BasePreprocess):
    def __init__(self, args):
        super(CasPreprocess, self).__init__(args)
        self.label_dimension = args['label_dimension']

    def _load_data(self, path):
        if self.args['split_criteria'] == 'dependent':
            # TODO: 目前是随机找了一个被试的mat进行读取，但每一个被试其实有三个mat可以用作训练的,具体怎么使用需要参考文献
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject']))
            origin_data = scipy.io.loadmat(path)
            data, label = self._map_eeg2label(origin_data)

        elif self.args['split_criteria'] == 'independent':
            data = []
            label = []
            for i in os.listdir(self.folder)[:5]:
                if not i.endswith(".mat"): 
                    continue
                path = os.path.join(self.folder, i) 
                origin_data = scipy.io.loadmat(path)
                subData, subLabel = self._map_eeg2label(origin_data)
                data.extend(subData.tolist())
                label.extend(subLabel.tolist())
        else:
            raise ValueError(f"{self.args.name}, {self.args.split_criteria} should be dependent or independent")   
        return np.array(data), np.array(label)

    def _map_eeg2label(self, data):
        LENGTH = self.args.trim_length
        # CAS/preprocessed下的文件是将data和label合并存放，欠规整（data只读取前14维，最后一维重参考）
        # ! TODO: eeg = dict 
        labelMacro = data['label']
        
        eeg = []
        for k, v in data.items():
            if k == 'label':
                continue
            eeg.append(v[:, v.shape[1]-LENGTH:])

        label = []
        for ll in np.squeeze(labelMacro).tolist():
            label.append([ll] * LENGTH)
        
        return np.array(eeg, dtype=np.float16), np.array(label, dtype=np.uint8)
        

    def _preprocess(self, data):
        montage = mne.channels.read_custom_montage(self.args['location'],coord_frame='head')
        self.ch = self.args['channels']
        preprocess_data = []
        # 为了速度快，这里只跑两个全流程就返回了，仅供测试使用
        for sub_data in [data]:
            # step1: 数据处理
            info = mne.create_info(
                ch_names = self.ch,
                ch_types = ['eeg' for _ in range(14)], 
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

    def _split(self, data, origin_label):
        label = []
        for index, sub_data in enumerate(data):
            label.append(np.repeat(origin_label[index], sub_data.shape[1]))

        data = data[0]
        label = label[0]
        len_data = data.shape[1]
        self.split_proportion = self.args['split_proportion']
        train_feature = data[:, :int(len_data * self.split_proportion)]
        test_feature = data[:,int(len_data * self.split_proportion):]
        train_label = label[:int(len_data * self.split_proportion)]
        test_label = label[int(len_data * self.split_proportion):]
        return train_feature, test_feature, train_label, test_label
