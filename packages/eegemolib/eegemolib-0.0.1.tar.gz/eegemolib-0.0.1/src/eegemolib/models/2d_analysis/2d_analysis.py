"""
    mostly from https://github.com/High-East/BCI-ToolBox
"""

from .EEGNet import EEGNet
from .FBCNet import FBCNet
from .DeepConvNet import DeepConvNet
from .ShallowConvNet import ShallowConvNet
from .DGCNN import DGCNN
from .LSTM import Model as LSTM
from .sru import SRU, SRUCell
import torch


class twoD_analysis:
    """
        data for training: torch.tensor, in shape [batch, channel, (band, )feature/time]
    """
    def __init__(self, classes_num, params, feature_dim=-2, time_dim=-1):
        super(twoD_analysis, self).__init__()
        self.numClasses = classes_num
        self.params = params
        self.featureDIM = feature_dim
        self.timeDIM = time_dim
        self.classifier = None
        self.regressor = None

    def classify(self, data, label):
        train_data, train_label = self.reformat(data, label)

    def regress(self, data, label):
        pass

    def fit(self, data, method="classify"):
        if method == "classify":
            output = self.classifier.transform(data)
        else:
            assert method == "regress"
            output = self.regressor.transform(data)
        return output

    def reformat(self, data, label):
        data = torch.tensor(data)
        b = data.size(0)
        # Section: reformat input into [batch, num_features]
        data = data.squeeze().reshape([-1, data.size(self.featureDIM)])
        multiplied = data.size(0) // b
        label = label.repeat_interleave(multiplied)
        return data, label
