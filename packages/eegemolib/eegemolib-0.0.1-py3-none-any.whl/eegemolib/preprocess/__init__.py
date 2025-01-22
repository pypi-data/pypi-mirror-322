"""This package includes all the modules related to data loading and preprocessing

 To add a custom dataset class called 'dummy', you need to add a file called 'dummy_dataset.py' and define a subclass 'DummyDataset' inherited from BasePreprocess.
 You can implement five functions:
    -- <_load_data>:                      load data 根据路径加载EEG数据
    -- <_load_feature>:                   load features 根据路径加载EEG特征
    -- <_preprocess>:                     preprocess data 预处理流程
    -- <_feature_compute>:                compute features 根据compute_fea_list计算特征
    -- <_feature_selection>:              select features 特征选择
    -- <_split>:                          split train set and test set 划分训练集和测试集
"""
import importlib
from preprocess.base_preprocess import BasePreprocess

def find_model_using_name(model_name):
    """Import the module "preprocess/[dataset_name]_preprocess.py".

    In the file, the class called [dataset_name]() will
    be instantiated. It has to be a subclass of BasePreprocess,
    and it is case-insensitive.
    """
    model_filename = "preprocess." + model_name.lower() + "_preprocess"
    modellib = importlib.import_module(model_filename)
    model = None
    for name, module in modellib.__dict__.items():
        if name.lower() == (model_name.lower()+ 'preprocess') and issubclass(module, BasePreprocess):
            model = module
    if model is None:
        raise NotImplementedError(f"In {model_filename}.py, there should be a subclass of BasePreprocess with class name that matches {model_name + 'preprocess'} Preprocess in lowercase." )

    return model

def create_preprocess(args):
    model = find_model_using_name(args['name'])
    instance = model(args)
  
    print("[%s] was created" % (type(instance).__name__))
    instance.generate()
    return True

