from typing import List

import torch
import torch.nn as nn

from .layers import Conv2dWithConstraint, LinearWithConstraint

torch.set_printoptions(linewidth=1000)


# 5 layers of cnn
class DeepConvNet(nn.Module):
    def __init__(
            self,
            n_classes: int,
            input_shape: List[int],
            first_conv_length: int,
            block_out_channels: List[int],
            pool_size: int,
            weight_init_method=None,
    ) -> None:
        super(DeepConvNet, self).__init__()
        b, c, s, t = input_shape
        last_dim = max(1, t//(2**(len(block_out_channels)-1))) * block_out_channels[-1]   # divide pooling, multiply kernel num

        self.first_conv_block = nn.Sequential(
            nn.ZeroPad2d(((first_conv_length - 1) // 2, first_conv_length // 2, 0, 0)),
            Conv2dWithConstraint(1, block_out_channels[0], kernel_size=(1, first_conv_length), max_norm=2),
            Conv2dWithConstraint(block_out_channels[0], block_out_channels[1], kernel_size=(s, 1), bias=False,
                                 max_norm=2),
            nn.BatchNorm2d(block_out_channels[1]),
            nn.ELU(),
            nn.MaxPool2d((1, pool_size))
        )

        pool_list = []
        initial = t
        for _ in range(len(block_out_channels)-1):
            initial //= 2
            if initial > 1:
                pool_list.append(pool_size)
            else:
                pool_list.append(1)

        # print(pool_list)
        self.deep_block = nn.ModuleList(
            [self.default_block(block_out_channels[i - 1], block_out_channels[i], first_conv_length, pool_list[i-2]) for i in
             range(2, len(block_out_channels))]
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            LinearWithConstraint(last_dim, n_classes, max_norm=0.5)  # time points = 1125
        )
        # print(f'last dim = {last_dim}')

    def default_block(self, in_channels, out_channels, T, P):
        default_block = nn.Sequential(
            nn.ZeroPad2d(((T - 1) // 2, T // 2, 0, 0)),
            nn.Dropout(0.5),
            Conv2dWithConstraint(in_channels, out_channels, (1, T), bias=False, max_norm=2),
            nn.BatchNorm2d(out_channels),
            nn.ELU(),
            nn.MaxPool2d((1, P))
        )
        return default_block

    def forward(self, x):
        out = self.first_conv_block(x)
        # i = 0
        for block in self.deep_block:
            out = block(out)
            # i += 1
            # print(f'[{i}/{len(self.deep_block)}] blocks with out size = {out.size()}')
        out = self.classifier(out)
        return out
