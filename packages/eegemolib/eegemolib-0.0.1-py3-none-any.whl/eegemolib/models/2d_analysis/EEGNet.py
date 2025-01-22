# TODO: explain ip = https://zhkgo.github.io/2020/11/19/EEGNET%E7%BD%91%E7%BB%9C%E7%BB%93%E6%9E%84%E8%A7%A3%E6%9E%90
#  /#rewardModal
import torch.nn as nn
import torch.nn.functional as F

from models.base_model import BaseModel
from nn.layers import *


class EEGNet(BaseModel):
    def __init__(self, arg1, arg2):
        super(EEGNet, self).__init__(arg1, arg2)
        # model setting
        self._set_params(self.args)
        self.build_model()
        
    def _set_params(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)  
    
    def build_model(self):
        pooling_layer = nn.MaxPool2d(kernel_size=(2, 2))
        if self.F2 == 'auto':
            self.F2 = self.F1 * self.D

        # Spectral
        self.spectral = nn.Sequential(
            nn.Conv2d(1, self.F1, (1, self.T1), bias=False, padding='same'),
            nn.BatchNorm2d(self.F1))

        # Spatial
        self.spatial = nn.Sequential(
            Conv2dWithConstraint(self.F1, self.F1 * self.D, (1, self.s), bias=False, groups=self.F1),
            nn.BatchNorm2d(self.F1 * self.D),
            nn.ELU(),
            # pooling_layer((1, self.P1)),
            nn.Dropout(self.drop_out)
        )

        # Temporal
        self.temporal = nn.Sequential(
            nn.Conv2d(self.F1 * self.D, self.F2, (1, self.T2), bias=False, padding='same', groups=self.F1 * self.D),
            nn.Conv2d(self.F2, self.F2, 1, bias=False),
            nn.BatchNorm2d(self.F2),
            nn.ELU(),
            # pooling_layer((1, self.P2)),
            nn.Dropout(self.drop_out)
        )

        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            LinearWithConstraint(self.last_embedding, self.n_classes, max_norm=0.25) # self.last_embedding = 4960 for DEAP and 9760 for SEED
        )


    def forward(self, x):
        
        # x_reshape = x.reshape([x.size()[0],1, x.size()[-1]])
        out = self.spectral(x)
        out = self.spatial(out)
        out = self.temporal(out)
        out = self.classifier(out)
        return F.softmax(out, dim=1)      # after out     (batch size,    class number)
