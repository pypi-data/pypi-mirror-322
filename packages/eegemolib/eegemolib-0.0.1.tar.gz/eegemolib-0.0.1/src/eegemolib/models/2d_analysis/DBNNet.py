# TODO: explain ip = https://zhkgo.github.io/2020/11/19/EEGNET%E7%BD%91%E7%BB%9C%E7%BB%93%E6%9E%84%E8%A7%A3%E6%9E%90
#  /#rewardModal
import torch.nn as nn
import torch.nn.functional as F

from models.base_model import BaseModel
from nn.layers import *

class RBM(nn.Module):
    def __init__(self, visible_size, hidden_size):
        super(RBM, self).__init__()
        self.visible_size = visible_size
        self.hidden_size = hidden_size
        self.weights = nn.Parameter(torch.randn(self.visible_size, self.hidden_size))
        self.biases = nn.Parameter(torch.zeros(self.hidden_size))
    def forward(self, x):
        a = torch.matmul(x, self.weights) + self.biases
        b = torch.sigmoid(a)
        return b

class DBNNet(BaseModel):
    def __init__(self, arg1, arg2):
        super(DBNNet, self).__init__(arg1, arg2)
        # model setting
        self._set_params(self.args)
        self.build_model()
    
    def build_model(self):
        self.rbms = nn.Sequential(RBM(310, 64),
                RBM(64,16))

        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            LinearWithConstraint(16, 3, max_norm=0.25) # self.last_embedding = 4960 for DEAP and 9760 for SEED
        )

    def forward(self, x):
        # x_reshape = x.reshape([x.size()[0],1, x.size()[-1]])
        out = self.rbms(x)
        print(out.size())
        out = self.classifier(out)
        return F.softmax(out, dim=1)      # after out     (batch size,    class number)
