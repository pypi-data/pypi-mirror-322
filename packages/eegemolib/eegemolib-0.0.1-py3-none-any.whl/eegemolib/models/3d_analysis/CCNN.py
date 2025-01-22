import torch
import torch.nn as nn
from nn.conv import Conv
from models.base_model import BaseModel

class CCNN(BaseModel):
    def __init__(self, arg1, arg2):
        super(CCNN, self).__init__(arg1, arg2)
        self.Conv_1 = Conv(1, 64, k=3, s=1, p = 1, act='relu')
        self.Conv_2 = Conv(64, 128, k=3, s=1, p = 1,act='relu')
        self.Conv_3 = Conv(128, 256, k=3, s=1, p = 1,act='relu')
        self.Conv_4 = Conv(256, 64, k=1, s=1, act='relu')
        
        self.fc = nn.Sequential(
            nn.Linear(19840, 1024),
            nn.SELU(),
            nn.Dropout(0.5),
            nn.Linear(1024, 3)
        )
        
    def forward(self, x):
        x = self.Conv_1(x)
        x = self.Conv_2(x)
        x = self.Conv_3(x)
        x = self.Conv_4(x)
        # x = x.flatten(start_dim=1)
        x = x.view(x.size(0), -1)
        x = torch.softmax(self.fc(x), dim=1)
        return x
    

if __name__ == '__main__':
    # 写一段测试上面CCNN的代码
    model = CCNN().to('cuda')
    x = torch.randn(1, 4, 9, 9)
    x=x.to('cuda')
    y = model(x)
    print(y, y.shape)