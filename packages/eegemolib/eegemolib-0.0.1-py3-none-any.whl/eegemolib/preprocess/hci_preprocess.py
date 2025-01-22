import os
import scipy
import mne

from .base_preprocess import *
import xml.etree.ElementTree as ET
import numpy as np

def find_subject_mat(path, subject): # TODO 目前是随机找了一个被试的mat进行读取，但每一个被试其实有三个mat可以用作训练的
    # 一个文件夹下面有xxx_emotion.bdf, Sectio_x.tsv, Cut.tsv, session.xml，读取bdf文件
    target_file = os.listdir(os.path.join(path, str(subject))) [2]
    assert target_file, f"find_subject_mat(): no proper mat fit {subject}_xxx.mat in {path}"
    # print(target_file)
    return os.path.join(str(subject), target_file)

class HCIPreprocess(BasePreprocess):
    def __init__(self, args):
        super(HCIPreprocess, self).__init__(args)

    def _load_data(self, path):
        if self.args['split_criteria'] == 'dependent':
            # TODO: 目前是随机找了一个被试的mat进行读取，但每一个被试其实有三个mat可以用作训练的,具体怎么使用需要参考文献
            path = os.path.join(self.folder, find_subject_mat(self.folder, self.args['subject_id']))
            origin_data = mne.io.read_raw_bdf(path, preload=True).get_data()
            data = origin_data[:32, :]
            # TODO：HCI数据要根据时间戳切片，或可参考https://blog.csdn.net/qq_40995448/article/details/102499561?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-102499561-blog-110915137.235%5Ev43%5Epc_blog_bottom_relevance_base6&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-102499561-blog-110915137.235%5Ev43%5Epc_blog_bottom_relevance_base6&utm_relevant_index=2
            label = [self._find_subject_xml(self.folder, self.args['subject'])]

        elif self.args['split_criteria'] == 'independent':
            # TODO: 目前是把5个文件全都读进来了，这样测试的时间短一点，加载45个还是15个文件夹，需要找参考文献
            data = []
            label = []
            for i in os.listdir(self.folder)[:5]:
                if not i.endswith(".mat"): 
                    continue

                path = os.path.join(self.folder, i) 
                origin_data = scipy.io.loadmat(path)
                for key, value in origin_data.items():
                    if 'eeg' in key:
                        data.append(value)
                        label.append(label_mat[0][int(key.split('eeg')[1])-1])
        else:
            raise ValueError(f"{self.args[name]}, {self.args[split_criteria]} should be dependent or independent")   
        return data, label

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

    def _load_feature(self):
        pass

    def _find_subject_xml(self, path, subject): 
        # 一个文件夹下面有xxx_emotion.bdf, Sectio_x.tsv, Cut.tsv, session.xml，读取xml文件
        folder = os.path.join(path, str(subject))
        target_file = os.listdir(folder) [1]
        tree = ET.parse(os.path.join(folder,target_file))
        root = tree.getroot()

        # 获取session元素的属性值
        feltArsl = root.attrib.get('feltArsl')
        feltVlnc = root.attrib.get('feltVlnc')
        print(feltArsl)
        if int(feltArsl) <= 5:
            return 0
        else:
            return 1

    def _split(self, data, origin_label):
        label = []
        for index, sub_data in enumerate(data):
            label.append(np.repeat(origin_label[index], sub_data.shape[1]))

        data = data[0]
        label = label[0]
        len_data = data.shape[1]
        self.split_proportion = self.args['split_proportion']
        train_feature = data[:, :int(len_data * 0.8)]
        test_feature = data[:,int(len_data * 0.8):]
        train_label = label[:int(len_data * 0.8)]
        test_label = label[int(len_data * 0.8):]
        return train_feature, test_feature, train_label, test_label

