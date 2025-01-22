preprocess目录实现了常见EEG数据集（SEED、DEAP等）的数据读取、数据处理、特征计算、特征选择以及数据的划分（训练数据与测试数据的划分）。预处理的结果（train.cache, test.cache）会保存在"save_path"路径下

（1）xxx_preprocess.py 对应于xxx数据集的预处理过程,处理过程根据xxx数据集对应的yaml（./cfg/datasets/xxx.yaml）来制定的。
``` 
SEED_extracted_features.yaml与SEED_preprocess_EEG.yaml是可以合并的，参数都一样的，
为了举个yaml设置的例子，把使用预处理的EEG signal（对应SEED_preprocess_EEG.yaml）与预处理的特征（对应SEED_extracted_features.yaml）两种方式的yaml分开写了。
两者的主要区别在于“features”这个参数设置上，features是true说明输入的路径是预处理的特征的路径，feature_list可以提供特征的列表；false表示是预处理的EEG signal的路径。
``` 

> ##### <font face="Arial Unicode MS">Yaml Attributes描述</font>
>
> ```python
> - emotion_labels<list>:    情绪类别
> - emotion_names<list>:     情绪类别对应的名称
> - features<bool>:          是否使用数据集本身提供的特征，False 表示不使用，True 表示使用
> - feature_list<list>:      如果features=True,则对feature_list中的features进行读取
> - num_classes<int>:        类别数目
> - num_trials<int>:         试次数目
> - num_subjects<int>:       被试数目
> - num_sessions<int>:       实验重复数目
> - split_criteria<str>:     使用被试依赖还是被试独立 dependent/independent
> - subject_id<int>:         如果是被试依赖的设置，需要提供subject_id与session_id
> - session_id<int>:
> - subject_leave_id<int>:   如果是被试独立的设置，需要提供作为测试集的subject_id（在留一验证的情况下，具体要看数据集通用的划分方式是什么样的）
> - split_prop<float>:         如果是按照比例划分训练集与测试集，就按照split_prop来分
> - 后面的部分是预处理、特征计算、特征选择的一些具体参数设置
> ```

每个xxx_preprocess里都有xxx数据集对应的处理类，继承自BasePreprocess类（不知道这个描述对不对，没仔细看过python的语法，见谅）

（2）features.py实现了特征的计算，目前只有psd等几个特征，还没有把dev_zq与dev_wkr上的特征实现合并进来

（3）feature_selection.py 实现了一部分特征选择方法


数据集的位置在3090服务器上,路径为/data/shuyz/Emotion_compute/dataset,大家跑程序的时候最好不要直接访问我的数据集，可以复制一份数据集到自己的路径下，避免修改数据集。



