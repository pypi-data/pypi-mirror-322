"""Convolution modules.
    Reference link:https://github.com/ultralytics/ultralytics/blob/main/ultralytics/nn/modules/conv.py
"""
import math

import numpy as np
import torch
import torch.nn as nn
from .common import *

def autopad(k, p=None, d=1):  # kernel, padding, dilation
    """Pad to 'same' shape outputs."""
    if d > 1:
        k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
    if p is None:
        p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
    return p

class Conv(nn.Module):
    """ standard 2d convolution with args (ch_in, ch_out, kernel, stride, dilation, group, normalization, activation, bias)
        code: https://github.com/ultralytics/ultralytics/blob/main/ultralytics/nn/modules/conv.py
        args:
            ch_in(int): input channel
            ch_out(int): output channel
            kernel(int): kernel size
            stride(int): controls the stride for the cross-correlation
            dilation(int): space between the kernel points
            groups(int): divide ch_in and ch_out into several groups, ch_in % groups = 0, ch_out % groups = 0
            normalization(str): batchnorm or instance norm, use get_norm_layer() according to normalization input
            activation(str): activation function, use get_active_layer() according to activation input
            bias(bool): whether use bias in convolution, default True
        input:
            2d feature map: b * ch_in * h x w
        output:
            2d feature map: b * ch_out * (h / stride) * (w / stride)
    """
    def __init__(self, c_in, c_out, k, s, p=None, d=1, g=1, norm='batch', act='ReLU', b=True):
        super().__init__()
        # get norm and act function
        norm_func = get_norm_layer(norm)
        act_func = get_active_layer(act)
        # build layer
        self.conv = nn.Conv2d(c_in, c_out, k, s, autopad(k, p, d), groups=g, dilation=d, bias=b)
        self.norm = norm_func(c_out)
        self.act = act_func()

    def forward(self, x):
        return self.act(self.norm(self.conv(x)))


class ConvTranspose(nn.Module):
    """Convolution transpose 2d layer with args (ch_in, ch_out, kernel, stride, dilation, group, normalization, activation, bias)
        code: https://github.com/ultralytics/ultralytics/blob/main/ultralytics/nn/modules/conv.py
        args:
            ch_in(int): input channel
            ch_out(int): output channel
            kernel(int): kernel size
            stride(int): controls the stride for the cross-correlation
            dilation(int): space between the kernel points
            groups(int): divide ch_in and ch_out into several groups, ch_in % groups = 0, ch_out % groups = 0
            normalization(str): batchnorm or instance norm, use get_norm_layer() according to normalization input
            activation(str): activation function, use get_active_layer() according to activation input
            bias(bool): whether use bias in convolution, default True
        input:
            2d feature map: b * ch_in * h * w
        output:
            2d feature map: b * ch_out * (h / stride) * (w / stride)
    """
    def __init__(self, c_in, c_out, k, s, p=0, norm='batch', act='ReLU', bias=True):
        """Initialize ConvTranspose2d layer with batch normalization and ReLU function."""
        super().__init__()
        # get norm and act function
        norm_func = get_norm_layer(norm)
        act_func = get_active_layer(act)

        self.conv_transpose = nn.ConvTranspose2d(c_in, c_out, k, s, p, bias=bias)
        self.norm = norm_func(c_out) 
        self.act = act_func()

    def forward(self, x):
        """Applies transposed convolutions, batch normalization and activation to input."""
        return self.act(self.norm(self.conv_transpose(x)))

class DWConv(nn.Module):
    """ Depthwise Separable Convolution, DWConv(ch_in, ch_out)
    paper: Deep Learning with Depthwise Separable Convolutions
    code: https://blog.csdn.net/weixin_47414034/article/details/125922622
    args:
        ch_in(int): input channel
        ch_out(int): output channel
    input:
        x: b * ch_in * h * w
    output:
        x: b * ch_out * h * w
    """
    def __init__(self, ch_in, ch_out):
        super().__init__()
        self.depth_conv = nn.Conv2d(ch_in, ch_in, k=3, stride=1, padding = (k-1) // 2, groups=ch_in)
        self.width_conv = nn.Conv2d(ch_in, ch_out, k=1, stride=1, padding = (k-1) // 2, groups=1)
    def forward(self, x):
        return self.width_conv(self.depth_conv(x))

class ChannelAttention(nn.Module):
    """Channel Attention implement, 
    paper: Squeeze-and-Excitation Networks
    code: https://github.com/moskomule/senet.pytorch/blob/master/senet/se_module.py
    args:
        channel(int): channel of input feature map
        reduction(int): compress channel information from channel to (channel / reduction), then back to channel
    input:
        x: b * c * h * w
    output:
        x: b * c * h * w
    """
    def __init__(self, channel: int, reduction: int =16):
        super().__init__()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y

class SpatialAttention(nn.Module):
    """Spatial-attention module
    paper: CBAM: Convolutional Block Attention Module
    code: https://github.com/Jongchan/attention-module/blob/5d3a54af0f6688bedca3f179593dff8da63e8274/MODELS/cbam.py#L72
    args:
        k(int): kernel size
    input:
        x: b * c * h * w
    output:
        x: b * c * h * w
    """
    def __init__(self, k=7):
        super().__init__()
        assert k in {3, 7}, "kernel size must be 3 or 7 in SpatialAttention"
        self.conv = nn.Conv2d(2, 1, k, stride=1, padding = (k-1) // 2, bias=False)
        self.act = nn.Sigmoid()


    def forward(self, x):
        concat_x = torch.cat([torch.mean(x, 1, keepdim=True), torch.max(x, 1, keepdim=True)[0]], 1)
        return x * self.act(self.conv(concat_x))

class CBAM(nn.Module):
    """Convolutional Block Attention Module.
    paper: CBAM: Convolutional Block Attention Module
    code: https://github.com/Jongchan/attention-module/blob/5d3a54af0f6688bedca3f179593dff8da63e8274/MODELS/cbam.py#L72
    args:
        c(int): channel
        k(int): kernel size
    input:
        x: b * c * h * w
    output:
        x: b * c * h * w
    """
    def __init__(self, c, reduction=16, k=7):
        """Initialize CBAM with given input channel  and kernel size."""
        super().__init__()
        self.channel_attention = ChannelAttention(c, reduction)
        self.spatial_attention = SpatialAttention(k)

    def forward(self, x):
        return self.spatial_attention(self.channel_attention(x))

#####################  Conv Block ########################

class ResNetBlock(nn.Module):
    """ResNet block with standard convolution layers, ResNetBlock(ch_in, ch_out, s).
    paper: https://arxiv.org/pdf/1512.03385.pdf
    code: https://github.com/akamaster/pytorch_resnet_cifar10/blob/master/resnet.py
    args:
        ch_in(int): input channel
        ch_out(int): output channel
        s(int): stride
    input:
        x: b * c * h * w
    output: 
        x: b * c * (h / stride) * (w / stride)
    """
    def __init__(self, ch_in, ch_out, s=1):
        """Initialize convolution with given parameters."""
        super().__init__()
       
        self.conv1 = Conv(ch_in, ch_out, k=3, s=s, act='ReLU')
        self.conv2 = Conv(ch_out, ch_out, k=3, s=s, act='None')
        self.shortcut = nn.Sequential()
        self.act = nn.ReLU()

    def forward(self, x):
        """Forward pass through the ResNet block."""
        out = self.conv2(self.conv1(x))
        out = self.shortcut(x) + out
        return self.act(out)
