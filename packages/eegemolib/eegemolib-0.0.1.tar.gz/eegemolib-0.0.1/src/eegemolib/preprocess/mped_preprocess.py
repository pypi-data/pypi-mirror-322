import os
import scipy
import numpy as np
import mne

from .base_preprocess import Preprocess

def find_subject_mat(path, subject): # TODO 目前是随机找了一个被试的mat进行读取，但每一个被试其实有三个mat可以用作训练的
    files = [personName for personName in os.listdir(path) if os.path.isdir(os.path.join(path, personName))]   
    assert 0 <= subject < len(files)
    target_person = files[subject]
        
    return os.path.join(path, target_person), target_person
    
class MpedPreprocess(BasePreprocess):
    def __init__(self, args):
        super(MpedPreprocess, self).__init__(args)
        self.label_dimension = args['label_dimension']

    def _parse_data(self, person_name):
        LENGTH = self.args['trim_length']
        sub_dir = os.path.join(self.folder, person_name)
        labelMacro = scipy.io.loadmat(os.path.join(self.folder, 'raw_EEG_Label.mat'))['eeg_label']

        mat_1 = scipy.io.loadmat(os.path.join(sub_dir, f'{person_name}_d.mat')) # {'__header__': b'MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: Tue Feb 06 15:42:29 2018', '__version__': '1.0', '__globals__': [], 'raw_eeg1': array(xxx)}
        mat_2 = scipy.io.loadmat(os.path.join(sub_dir, f'{person_name}_dd.mat'))

        del mat_1['__header__']
        del mat_1['__version__']
        del mat_1['__globals__']
        del mat_2['__header__']
        del mat_2['__version__']
        del mat_2['__globals__']
        eeg = []
        for k, v in mat_1.items():
            eeg.append(v[:, v.shape[1]-LENGTH:])
        for k, v in mat_2.items():
            eeg.append(v[:, v.shape[1]-LENGTH:])

        label = []
        for ll in np.squeeze(labelMacro).tolist():
            label.append([ll] * LENGTH)
            
        return np.array(eeg, dtype=np.float16), np.array(label, dtype=np.uint8)

    def _load_data(self, path):
        

        if self.args['split_criteria'] == 'dependent':
            # TODO: 目前是随机找了一个被试的mat进行读取，但每一个被试其实有三个mat可以用作训练的,具体怎么使用需要参考文献
            path, person_name = find_subject_mat(self.folder, self.args['subject'])
            data, label = self._parse_data(person_name)
            
        elif self.args['split_criteria'] == 'independent':
            # TODO: 目前是把5个文件全都读进来了，这样测试的时间短一点，加载45个还是15个文件夹，需要找参考文献
            data = []
            label = []
            for i in range(5):
                path, person_name = find_subject_mat(self.folder, i)
                subData, subLabel = self._parse_data(person_name)
                data.extend(subData.tolist())
                label.extend(subLabel.tolist())
        else:
            raise ValueError(f"{self.args.name}, {self.args.split_criteria} should be dependent or independent")   
        return np.array(data), np.array(label)

    def _preprocess(self, data):
        montage = mne.channels.read_custom_montage(self.args['location'],coord_frame='head')
        self.ch = self.args['channels']
        preprocess_data = []
        # 为了速度快，这里只跑两个全流程就返回了，仅供测试使用
        for sub_data in [data]:
            # step1: 数据处理
            info = mne.create_info(
                ch_names = self.ch,
                ch_types = ['eeg' for _ in range(self.args['channelsInFile'])], 
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