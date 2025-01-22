import torch.nn as nn
import torch


class OutLayer(nn.Module):
    def __init__(self, d_in, d_hidden, d_out, time_len, dropout=.5, bias=.0):
        super(OutLayer, self).__init__()
        self.d_in, self.d_out, self.d_hidden = d_in, d_out, d_hidden
        self.fc_1 = nn.Sequential(nn.Linear(d_in, d_hidden), nn.ReLU(False), nn.Dropout(dropout), nn.BatchNorm1d(d_hidden))
        self.fc_2 = nn.Sequential(nn.Linear(d_hidden, d_out), nn.BatchNorm1d(d_hidden))
        self.fc_3 = nn.Sequential(nn.Linear(time_len * d_out, d_out), nn.Sigmoid())
        # self.fc = nn.Sequential(nn.Linear(time_len * d_in, d_out), nn.Sigmoid())
        self.fc = nn.Sequential(nn.Linear(d_in, d_out), nn.Sigmoid())
        # nn.init.constant_(self.fc_3[0].bias.data, bias)

    def forward(self, x):
        # TODO: attention in feature level + attention in time step level
        # print('>>>', x.size(), self.d_in, self.d_hidden)
        y = self.fc_1(x)
        y = self.fc_2(y)
        # TODO: concatenate time steps to one
        # print('> [LSTM OUTLayer] After fc_2:', y.size())
        y = torch.flatten(y, 1)
        # print('> [LSTM OUTLayer] After flatten', y.size())
        y = self.fc_3(y)
        # y = torch.flatten(x, 1)
        # y = self.fc(y)
        return y


class Model(nn.Module):
    def __init__(self, ori_feat_num, sel_feat_num, time_len, n_layers=1, bi=False, fc_hidden=15, emo_kinds=2, dropout=0.0):
        super(Model, self).__init__()
        self.inp = nn.Linear(ori_feat_num, ori_feat_num, bias=False)

        self.rnn = nn.LSTM(input_size=ori_feat_num, hidden_size=sel_feat_num, bidirectional=bi,
                           num_layers=n_layers, batch_first=True)

        d_rnn_out = sel_feat_num * (int(bi)+1)
        self.out = OutLayer(time_len, fc_hidden, emo_kinds, time_len=d_rnn_out, dropout=dropout)

    def forward(self, x):
        # FIXME: torch.Size([BATCH, 70, 42])
        # x = self.inp(x)
        # FIXME: torch.Size([BATCH, 70, 20])
        x, (h_n, c_n) = self.rnn(x)
        # h_n = h_n.permute(1, 0, 2)
        # FIXME: torch.Size([BATCH, STEP=70, 1])
        # TODO: flatten or just use the last step
        # y = self.out(h_n)
        y = self.out(x.permute(0, 2, 1))
        return y
