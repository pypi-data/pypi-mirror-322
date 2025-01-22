import os
import scipy
import mne
import re

from .base_preprocess import *

def find_subject_mat(path, subject_id, session_id):
    files = os.listdir(os.path.join(path, str(session_id)))  
    target_file = next((f for f in files if f.startswith(f"{subject_id}_")), None)  
    assert target_file, f"find_subject_mat(): no proper mat fit {subject_id}_xxx .mat in {path}"
    return os.path.join(str(session_id), target_file)


def find_session_label(session_id):
    # SEEDIV中每个session对应的label不一样
    if session_id == 1:
        return [1,2,3,0,2,0,0,1,0,1,2,1,1,1,2,3,2,2,3,3,0,3,0,3]
    elif session_id == 2:
        return [2,1,3,0,0,2,0,2,3,3,2,3,2,0,1,1,2,1,0,3,0,1,3,1]
    elif session_id == 3:
        return [1,2,2,1,3,3,3,1,1,2,1,0,2,3,3,0,2,3,0,0,2,0,1,0]
    else:
        raise ValueError(f"session_id should be in range in find_session_label")  
    
class SeedIVPreprocess(BasePreprocess):
    def __init__(self, args):
        super(SeedIVPreprocess, self).__init__(args)

    def _load_data(self, path):
        if self.args['split_criteria'] == 'dependent':
            # 对于被试依赖的设置，需要根据yaml中的session_id, subject_id获取对应的数据
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject_id'], self.args['session_id']))
            origin_data = scipy.io.loadmat(path)
            data = [value for key, value in origin_data.items() if 'eeg' in key]
            label = find_session_label(self.args['session_id'])
        elif self.args['split_criteria'] == 'independent':
            # TODO: 目前是把前6个文件全都读进来了，这样测试的时间短一点，加载45个还是15个文件夹，需要进一步找参考文献，目前用的是45个文件
            data = []
            label = []
            files = np.concatenate([os.listdir(os.path.join(self.folder, str(i + 1))) for i in range(self.args['num_sessions'])], axis=0)
            sorted_files = sorted(files, key=lambda x: int(x.split('_')[0]))
            for index, i in enumerate(sorted_files[:6]):
                path = os.path.join(self.folder, os.path.join(str(index % self.args['num_sessions'] + 1), i)) 
                origin_data = scipy.io.loadmat(path)
                for key, value in origin_data.items():
                    if 'eeg' in key:
                        data.append(value)
                        label.append(find_session_label(index % self.args['num_sessions'] + 1))
        else:
            raise ValueError(f"{self.args[name]}, {self.args[split_criteria]} should be dependent or independent")   
        return data, label

    def _load_feature(self,  data, feature_list):
        data_dict = {key: [] for key in feature_list}
        label = []
        if self.split_criteria == 'dependent':
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject_id'], self.args['session_id']))
            origin_fea = scipy.io.loadmat(path)
            for i in range(self.args['num_trials']):
                for key, value in sorted(origin_fea.items()):
                    if re.findall(r'\d+', key) and int(re.findall(r'\d+', key)[0]) == (i + 1) and re.sub(r'\d+', '', key) in self.args['feature_list']:
                       data_dict[re.sub(r'\d+', '', key)].append(value)
                label = find_session_label(self.args['session_id'])
        elif self.split_criteria == 'independent':
            # TODO: 目前是把前6个特征文件全都读进来了，这样测试的时间短一点，加载45个还是15个文件，需要进一步找参考文献，目前用的是45个文件
            data = []
            label = []
            files = np.concatenate([os.listdir(os.path.join(self.folder, str(i + 1))) for i in range(self.args['num_sessions'])], axis=0)
            sorted_files = sorted(files, key=lambda x: int(x.split('_')[0]))
            for index, i in enumerate(sorted_files[:6]):
                path = os.path.join(self.folder, os.path.join(str(index % self.args['num_sessions'] + 1), i)) 
                origin_fea = scipy.io.loadmat(path)
                for i in range(self.args['num_trials']):
                    trial_fea = []
                    for key, value in origin_fea.items():
                        if re.findall(r'\d+', key) and int(re.findall(r'\d+', key)[0]) == (i + 1) and re.sub(r'\d+', '', key) in self.args['feature_list']:
                            value_transpose = np.transpose(value, axes=(0,2,1))
                            trial_fea.append(value_transpose.reshape(-1, value.shape[1]))

                    trial_fea = np.concatenate(trial_fea, axis=0)
                    data.append(trial_fea)
                    label.append(find_session_label(self.args['session_id']))
        else:
            raise ValueError(f"{self.args[name]}, {self.args[split_criteria]} should be dependent or independent")   

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
            # SEED-IV 数据集被试依赖的划分是把24个trial中16个划分为训练集，8个划分为测试集
            # 参考论文《EmotionMeter: A Multimodal Framework for Recognizing Human Emotions》，为了平均数据，我们按照情绪类别的进行划分，积极、消极、中性情绪的前4个trial为训练集，后2个trial为测试集
            # shuffle data
            if self.args['split_shuffle']: # default False
                np.random.shuffle(data)
                np.random.shuffle(label)
            train_indices = []
            test_indices = []
            for i, num in enumerate(label):
                if label[:i+1].count(num) <= 4:
                    train_indices.append(i)
                else:
                    test_indices.append(i)

            train_label = []
            test_label = []
            train_feature = [data[i] for i in train_indices]
            _train_label = [label[i] for i in train_indices]
            test_feature = [data[i] for i in test_indices]
            _test_label = [label[i] for i in test_indices]

            for index, sub_feature in enumerate(train_feature):
                train_label.append(np.repeat(_train_label[index], sub_feature.shape[1]))
            for index, sub_feature in enumerate(test_feature):
                test_label.append(np.repeat(_test_label[index], sub_feature.shape[1]))
            
            train_feature = np.concatenate(train_feature, axis=1)
            train_label = np.concatenate(train_label, axis=0)
            test_feature = np.concatenate(test_feature, axis=1)
            test_label = np.concatenate(test_label, axis=0)
        elif self.split_criteria == 'independent':
            print(len(data))
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
            raise ValueError(f"{self.args[name]}, {self.args[split_criteria]} should be dependent or independent")   

        return train_feature, test_feature, train_label, test_label



