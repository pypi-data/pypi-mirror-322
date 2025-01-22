import importlib
from torch import nn
from models.base_model import BaseModel
def find_model_using_name(model_name, model_type):
    """Import the module "models/[model_name]_model.py".

    In the file, the class called DatasetNameModel() will
    be instantiated. It has to be a subclass of BaseModel,
    and it is case-insensitive.
    """
    model_filename = "models." + model_type.lower() + "_analysis." + model_name # 先用2维的analysis做个测试，后面可以自定义寻找目录
    modellib = importlib.import_module(model_filename)
    model = None
    target_model_name = model_name
    for name, cls in modellib.__dict__.items():
        if name.lower() == target_model_name.lower() \
           and issubclass(cls, BaseModel):
            model = cls

    if model is None:
        print("In %s.py, there should be a subclass of BaseModel with class name that matches %s in lowercase." % (model_filename, target_model_name))
        exit(0)

    return model

def create_model(model_name, model_type):
    model = find_model_using_name(model_name[:-5], model_type)
    instance = model(model_name, model_type)
    # print(instance.args)
    print("[%s]: model [%s] was created" % (model_type, type(instance).__name__))
    return instance
