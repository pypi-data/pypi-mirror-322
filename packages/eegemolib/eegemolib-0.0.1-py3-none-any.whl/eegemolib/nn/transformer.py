""" transformer modules.
"""
import math

import numpy as np
import torch
import torch.nn as nn
from .common import *

class PositionalEncoding(nn.Module):

    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()       
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        # div_term = torch.exp(
        #     torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        # )
        div_term = 1 / (10000 ** ((2 * np.arange(d_model)) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term[0::2])
        pe[:, 1::2] = torch.cos(position * div_term[1::2])

        pe = pe.unsqueeze(0).transpose(0, 1) # [5000, 1, d_model],so need seq-len <= 5000
        #pe.requires_grad = False
        self.register_buffer('pe', pe)

    def forward(self, x):
        # print(self.pe[:x.size(0), :].repeat(1,x.shape[1],1).shape ,'---',x.shape)
        # dimension 1 maybe inequal batchsize
        return x + self.pe[:x.size(0), :].repeat(1,x.shape[1],1)

class Transformer(nn.Module):
    """
    transformer encoder and decoder, args ()
    code: https://github.com/oliverguhr/transformer-time-series-prediction/blob/master/transformer-singlestep.py

    """
    def __init__(self, ch_in, n_layers=1, dropout=0.1):
        super().__init__()
        # TODO: embedding层放在哪里比较合适？transformer一开始是肯定要一个embedding层的，全连接或者其他的形式
        # self.input_embedding  = nn.Linear(1,feature_size)
        self.pos_encoder = PositionalEncoding(ch_in)
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=ch_in, nhead=8, dropout=dropout)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=n_layers)
        # TODO: 这个decoder是不是一定要加
        self.decoder = nn.Linear(ch_in,1)

    def forward(self, x):
        # src with shape (input_window, batch_len, 1)
        if self.src_mask is None or self.src_mask.size(0) != len(src):
            device = src.device
            mask = self._generate_square_subsequent_mask(len(src)).to(device)
            self.src_mask = mask
        x = self.pos_encoder(x)
        output = self.transformer_encoder(x, self.src_mask)#, self.src_mask)
        output = self.decoder(output)
        return output

    def _generate_square_subsequent_mask(self, sz):
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask
