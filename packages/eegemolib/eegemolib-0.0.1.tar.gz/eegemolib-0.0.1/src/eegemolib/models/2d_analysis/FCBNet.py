# https://arxiv.org/pdf/2104.01233.pdf

# import sys
import torch.nn as nn
from torch.nn import functional as F

from models.base_model import BaseModel
from nn.layers import *


class FCBNet(BaseModel):
    def __init__(self, arg1, arg2):
        super(FCBNet, self).__init__(arg1, arg2)
        # model setting
        self._set_params(self.args)
       
        # SCB (Spatial Convolution Block)
        self.scb = nn.Sequential(
            Conv2dWithConstraint(self.n_band, self.m * self.n_band, (1, self.n_electrode), groups=self.n_band, max_norm=2),
            nn.BatchNorm2d(self.m * self.n_band),
            Swish()
        )

        # Temporal Layer
        self.temporal_layer = LogVarLayer(-1)

        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            LinearWithConstraint(self.n_band * self.m * self.temporal_stride, self.n_classes, max_norm=0.5)
        )
    def _set_params(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)  

    def forward(self, x):
        out = self.scb(x)
        out = F.pad(out, (0, 3))
        out = out.reshape([*out.shape[:2], self.temporal_stride, int(out.shape[-1] / self.temporal_stride)])
        out = self.temporal_layer(out)
        out = self.classifier(out)
        return out
