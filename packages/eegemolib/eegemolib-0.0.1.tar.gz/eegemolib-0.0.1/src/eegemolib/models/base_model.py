import os
import torch
from abc import ABC, abstractmethod
from utils.utils import load_yaml, check_yaml
from torch import nn

class BaseModel(nn.Module):
    def __init__(self, model_name, model_type):
        super(BaseModel, self).__init__()

        self.cfg = './cfg/models/' + model_type + '/' + model_name
        if check_yaml(self.cfg):
            self.args = load_yaml(self.cfg) # load model args according given model
        else:
            print("there should be a .yaml file matches %s in lowercase." % (self.cfg))
            exit(0)

    @abstractmethod
    def build_model(self):
        pass

    @abstractmethod
    def _set_params(self, kwargs):
        pass

    @abstractmethod
    def forward(self):
        pass