# https://arxiv.org/pdf/2104.01233.pdf

# import sys
import torch.nn as nn
from torch.nn import functional as F

from models.base_model import BaseModel
from nn.layers import *


class TSception(BaseModel):
    def __init__(self, arg1, arg2):
        super(TSception, self).__init__(arg1, arg2)
        # model setting
        self._set_params(self.args)
       
        self.inception_window = [0.5, 0.25, 0.125]
        self.pool = 8

        self.Tception1 = self.conv_block(1, self.num_T, (1, int(self.sampling_rate * self.inception_window[0])),
                                         1, self.pool, self.activation, self.pooling_type)
        self.Tception2 = self.conv_block(1, self.num_T, (1, int(self.sampling_rate * self.inception_window[1])),
                                            1, self.pool, self.activation, self.pooling_type)
        self.Tception3 = self.conv_block(1, self.num_T, (1, int(self.sampling_rate * self.inception_window[2])),
                                            1, self.pool, self.activation,self.pooling_type)
        
        self.Sception1 = self.conv_block(self.num_T, self.num_S, (1, self.input_size[1],), 1, 2, self.activation, self.pooling_type)
        self.Sception2 = self.conv_block(self.num_T, self.num_S, (1, int(self.input_size[1] * 0.5)), (int(self.input_size[1] * 0.5), 1), 2, self.activation, self.pooling_type)

        self.fusion_layer = self.conv_block(self.num_S, self.num_S, (1, 3), 1, 4, self.activation, self.pooling_type)

        self.BN_1 = nn.BatchNorm2d(self.num_T)
        self.BN_2 = nn.BatchNorm2d(self.num_S)
        self.BN_3 = nn.BatchNorm2d(self.num_S)

        self.fc = nn.Sequential(
            nn.Linear(self.num_S, self.hidden_state),
            nn.ReLU(),
            nn.Dropout(self.dropout_rate),
            nn.Linear(self.hidden_state, self.num_classes)
        )

    def conv_block(self, in_channels, out_channels, kernel_size, stride, pool, activation, pooling_type):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, stride),
            nn.LeakyReLU() if activation == 'leaky_relu' else nn.ReLU(),
            nn.AvgPool2d(kernel_size=(1, pool), stride=(1, pool)) if pooling_type == 'avg' else nn.MaxPool2d(kernel_size=(1, pool), stride=(1, pool))
        )
    
    def _set_params(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)  

    def forward(self, x):
        x1 = self.Tception1(x)
        out = x1
        x2 = self.Tception2(x)
        print(out.size(), x2.size())
        out = torch.cat((out, x2), dim=3)
        x3 = self.Tception3(x)
        out = torch.cat((out, x3), dim=3)

        x = out
        x = self.BN_1(x)

        x1 = self.Sception1(x)
        x2 = self.Sception2(x)
        
        x = torch.cat((x1, x2), 3)
        x = self.BN_2(x)

        x = self.fusion_layer(x)
        x = self.BN_3(x)

        x = torch.squeeze(torch.mean(x, -1), -1)
        x = self.fc(x)

        return x
