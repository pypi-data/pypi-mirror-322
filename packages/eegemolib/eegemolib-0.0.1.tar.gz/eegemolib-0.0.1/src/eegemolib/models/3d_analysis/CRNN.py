import torch
import torch.nn as nn
from nn.conv import Conv
from nn.recurrent import Rnn
from models.base_model import BaseModel

class CRNN(BaseModel):
    def __init__(self, arg1, arg2):
        super(CRNN, self).__init__(arg1, arg2)
        self.conv = nn.Sequential(
            Conv(1, 64, k=3, s=1, p = 1, act='relu'),
            Conv(64, 128, k=3, s=1, p = 1,act='relu'),
            Conv(128, 256, k=3, s=1, p = 1,act='relu'),
            Conv(256, 64, k=1, s=1, act='relu'),
            nn.Linear(19840, 512)
        )
        # TODO: 这个地方是要多个conv的结果拼接以后再送到lstm里面去，还没实现
        self.lstm =  Rnn('lstm',128, 512,64,3)
        self.fc = nn.Sequential(
            nn.Linear(1024, 3)
        )
    def forward(self, x):
        out = self.conv(x)
        out = self.lstm(out)
        out = self.fc(out)

        return out

       
    

if __name__ == '__main__':
    # 写一段测试上面CRNN的代码
    model = CRNN().to('cuda')
    x = torch.randn(1, 4, 9, 9)
    x=x.to('cuda')
    y = model(x)
    print(y, y.shape)