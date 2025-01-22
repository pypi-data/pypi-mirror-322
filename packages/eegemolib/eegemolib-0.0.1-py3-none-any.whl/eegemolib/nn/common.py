import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler

###############################################################################
# Helper Functions
# refer to cyclegan: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/models/networks.py
###############################################################################

class Identity(nn.Module):
    """ Identity mapping
        module = Identity()
        x = module(x) , where output = input

    args:
        x: input feature map
        
    intput: x 
    output: x
    """
    def forward(self, x):
        return x


def get_norm_layer(norm_type = 'batch'):
    """Return a normalization layer
    code: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/models/networks.py
    args:
        norm_type (str) -- the name of the normalization layer: batch | instance | none
        batch -> batch normalization
        instance -> instance normalization
        none -> without normalization

        For BatchNorm, we use learnable affine parameters and track running statistics (mean/stddev).
        For InstanceNorm, we do not use learnable affine parameters. We do not track running statistics.
        default use BatchNorm function
    input: 
        x
    output: 
        norm(x)
    """
    norm_type = norm_type.lower()
    if norm_type == 'batch':
        norm_layer = functools.partial(nn.BatchNorm2d, affine=True, track_running_stats=True)
    elif norm_type == 'instance':
        norm_layer = functools.partial(nn.InstanceNorm2d, affine=False, track_running_stats=False)
    elif norm_type == 'none':
        def norm_layer(x):
            return Identity()
    else:
        raise NotImplementedError('normalization layer [%s] is not found' % norm_type)
    return norm_layer

def get_active_layer(active_type = 'ReLU'):
    """Return a activation layer

    args:
        norm_type (str) -- the name of the activation layer: ReLU | LeakReLU | Sigmoid | Softmax
        default use ReLU activation function
    
    input: 
        x
    output: 
        activation(x)
    """
    active_type = active_type.lower()
    if active_type == 'relu':
        active_layer = functools.partial(nn.ReLU, inplace=False)
    elif active_type == 'leakyrelu':
        active_layer = functools.partial(nn.LeakyReLU, negative_slope=0.01, inplace=False)
    elif active_type == 'sigmoid':
        active_layer = functools.partial(nn.Sigmoid)
    elif active_type == 'softmax':
        active_layer = functools.partial(nn.Softmax)
    elif active_type == 'selu':
        active_layer = functools.partial(nn.SELU)
    elif active_type == 'none':
        def active_layer():
            return Identity()
    else:
        raise NotImplementedError(f'activation layer {active_type} is not found')
    return active_layer

def get_pool_layer(pool_type = 'ave'):
    """Return a pooling layer

    Args:
        pool_type (str): the type of pooling layer: ave (average pooling) | max (max pooling)
    Returns: 
        nn.Module: pooling layer
    input:
        x
    output: 
        pooling(x)
    """
    pool_type = pool_type.lower()
    if pool_type == 'ave':
        pool_layer = functools.partial(nn.AvgPool2d)
    elif pool_type == 'max':
        pool_layer = functools.partial(nn.MaxPool2d)
    elif pool_type == 'adaptiveave':
        pool_layer = functools.partial(nn.AdaptiveAvgPool2d)
    elif pool_type == 'adaptivemax':
        pool_layer = functools.partial(nn.AdaptiveMaxPool2d)
    else:
        raise NotImplementedError(f'pooling layer {pool_layer} is not found')
    return pool_layer

# TODO: dropout, embedding 
