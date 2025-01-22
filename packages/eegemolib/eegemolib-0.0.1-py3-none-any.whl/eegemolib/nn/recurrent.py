""" Recurrent modules """
import math
import torch.nn.functional as F
import numpy as np
import torch
import torch.nn as nn
from .common import *

class Rnn(nn.Module):
    """ standard recurrent unit with args (rnn_type, ch_in, ch_out, n_layers, bidirectional, dropout, batch_first, bias, nonlinearity), implement GRU, RNN and LSTM
    code: refer to https://github.com/Lizhen0628/text_classification/blob/master/model/models.py
    args: 
        rnn_type(str): recurrent module name, lstm/gru/rnn
        ch_in(int): input channel
        ch_out(int): output channel
        n_layers(int): the number of recurrent layer
        bidirectional(bool): whether use bidirectional recurrent module
        dropout(float): dropuut params, defaut use 0, i.e., without dropout
        batch_first(bool): whether bach_size is the first dimension of input feature map 
        bias(bool): whether us bias in recurrent module
        nonlinearity(str): active func, tanh/relu
    input:
        x: b * len * ch_in (batch_first=True) or len * b * ch_in (batch_first=False)
        h0: n_layers * b * ch_in (bidirectional=False) or (n_layers * 2) * b * ch_in (bidirectional=True), Defaults to zeros if not provided.
        c0: n_layers * b * ch_in (bidirectional=False) or (n_layers * 2) * b * ch_in (bidirectional=True), Defaults to zeros if not provided.
    output:
        x: b * len * ch_out (batch_first=True, bidirectional=False) or b * len * (2 *ch_out) (batch_first=True, bidirectional=True)
           len * b * ch_in (batch_first=False, bidirectional=False) or len * b * (2 *ch_out) (batch_first=True, bidirectional=True)
        hidden: n_layers * b * ch_out (bidirectional=False) or (n_layers * 2) * b * ch_out (bidirectional=True), containing the final hidden state for each element in the batch.
        cell: n_layers * b * ch_out (bidirectional=False) or (n_layers * 2) * b * ch_out (bidirectional=True), containing the initial cell state for each element in the input sequence
    """
    def __init__(self, rnn_type, ch_in, ch_out, n_layers, bidirectional=False, dropout=0, batch_first=True, bias=True, nonlinearity='tanh'):
        super().__init__()
        self.rnn_type = rnn_type.lower()
        if self.rnn_type == 'lstm':
            self.rnn = nn.LSTM(ch_in,
                               ch_out,
                               num_layers=n_layers,
                               bidirectional=bidirectional,
                               batch_first=batch_first,
                               dropout=dropout,
                               bias=bias)
        elif self.rnn_type == 'gru':
            self.rnn = nn.GRU(ch_in,
                              ch_out,
                              num_layers=n_layers,
                              bidirectional=bidirectional,
                              batch_first=batch_first,
                              dropout=dropout,
                              bias=bias)
        else:
            self.rnn = nn.RNN(ch_in,
                              ch_out,
                              num_layers=n_layers,
                              bidirectional=bidirectional,
                              batch_first=batch_first,
                              dropout=dropout,
                              bias=bias,
                              nonlinearity=nonlinearity)

    def forward(self, x):
        # TODO: 这里默认h0,c0都是0了，没有做特殊的处理
        if self.rnn_type in ['rnn', 'gru']:
            x, hidden = self.rnn(x)
            return x, hidden
        else:
            x, (hidden, cell) = self.rnn(x)
            return x, hidden, cell


class ResidualLSTM(nn.Module):
    """
    residual LSTM implement, ch_in, ch_out, n_layers, bidirectional, dropout, batch_first, bias
    paper: Residual LSTM: Design of a Deep Recurrent Architecture for Distant Speech
Recognition
    code: https://github.com/sidharthgurbani/HAR-using-PyTorch/blob/master/Bidir_Res_LSTM/model.py
    args: the same as RNN
    input: the same as RNN
    output: 
        x: hidden states of all timesteps for the last layer(batch_size, max_seq_len, hidden_size) 
        hidden: list of last hidden states for each layer n_layers * (1, batch_size, hidden_size) 
        cell: list of last cell states for each layer n_layers * (1, batch_size, hidden_size) 
    """
    def __init__(self, ch_in, ch_out, n_layers, bidirectional=True, dropout=0, batch_first=True, bias=True):
        super().__init__()
        self.drop_prob = dropout
        act_func = get_active_layer('relu')
        self.bidir_lstm1 = Rnn('lstm', ch_in, int(ch_out / 2), n_layers, bidirectional=True, dropout=self.drop_prob, batch_first=batch_first, bias=bias)
        self.bidir_lstm2 = Rnn('lstm', ch_in, int(ch_out / 2), n_layers, bidirectional=True, dropout=self.drop_prob, batch_first=batch_first, bias=bias)
        # TODO: 这个地方要不要结合到get_norm_layer()的函数里面？看起来会统一一点
        self.norm = nn.BatchNorm1d(ch_out)
        self.act = act_func()

    def forward(self, x):
        # TODO: 这里默认h0,c0都是0了，没有做特殊的处理
        mid_layer1, hidden_layer1, cell_layer1 = self.bidir_lstm1(x)
        mid_layer1 = self.act(mid_layer1)
        output_layer1, hidden_layer2, cell_layer2 = self.bidir_lstm2(mid_layer1)
        output_layer1 = self.act(output_layer1)

        mid_layer2 = mid_layer1 + output_layer1
        output = self.norm(mid_layer2)
        return output


class AttentionLSTM(nn.Module):
    """
    attention based lstm, with args(ch_in, ch_out, n_layers, bidirectional=True, dropout=0, batch_first=True, bias=True)
    code:https://github.com/slaysd/pytorch-sentiment-analysis-classification/blob/master/model.py
    args: the same as lstm
    input: the same as lstm
    output: the same as lstm
    """
    def __init__(self, ch_in, ch_out, n_layers=1, bidirectional=True, dropout=0, batch_first=True, bias=True):
        super().__init__()
        # TODO: n_layers > 1的实现还没做，没有找到对应的文献
        assert n_layers == 1, "AttentionLSTM should set n_layers=1"
        self.drop_prob = dropout
        self.bidir_lstm = Rnn('lstm', ch_in, int(ch_out / 2), n_layers, bidirectional=True, dropout=self.drop_prob, batch_first=batch_first, bias=bias)

    def attention(self, lstm_output, final_state):
        merged_state = torch.cat([s for s in final_state], 1)
        merged_state = merged_state.squeeze(0).unsqueeze(2)
        weights = torch.bmm(lstm_output, merged_state)
        weights = F.softmax(weights.squeeze(2), dim=1).unsqueeze(2)
        return torch.bmm(torch.transpose(lstm_output, 1, 2), weights).squeeze(2)

    def forward(self, x):
        # TODO: 这里默认h0,c0都是0了，没有做特殊的处理
        output, hidden, cell = self.bidir_lstm(x)
        # attn_output = self.attention_net(output, hidden)
        attn_output = self.attention(output, hidden)

        return attn_output.squeeze(0)