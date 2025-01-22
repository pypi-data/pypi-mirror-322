""" Linear modules """

import torch.nn as nn
from .common import *

class MLP(nn.Module):
    """ Multi-layer perceptron, MLP(channels, normalization, activation, bias)
    args:
        ch(list): a list of channels
        norm(str): normalization function
        act(str): activation function
        bias(bool): whether use bias in linear layer, defaut True
    input:
        x: b * channels[0]
    output:
        x: b * channels[-1]
    """
    def __init__(self, ch: list, norm='batch', act='ReLU', b=True):
        super().__init__()
        n = len(ch)
        layers = []
        norm_func = get_norm_layer(norm)
        act_func = get_active_layer(act)
        for i in range(1, n):
            layers.append(
                nn.Linear(ch[i - 1], ch[i], bias=b))
            if i < (n - 1):
                layers.append([
                    norm_func(ch[i]),
                    act_func()
                ])  
        self.mlp = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.mlp(x)  