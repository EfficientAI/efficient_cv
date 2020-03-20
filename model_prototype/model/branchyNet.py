import os
import sys
#import numpy as np

import torch
import torch.nn as nn
#from torch.autograd import Variable

sys.path.append(os.path.abspath('.'))
#from utils.utils import stringify


is_cuda = torch.cuda.is_available()
device = torch.device("cuda" if is_cuda else "cpu")


class model(nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.conv_block1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.conv_block2 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=32, kernel_size=3),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.conv_block3 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3),
            nn.BatchNorm2d(128),
            nn.ReLU(),
        )
        self.conv_block4 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.exit_path1 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=8, kernel_size=3),
            nn.BatchNorm2d(8),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.Dropout(p=0.2),
            nn.Linear(1352, 10),
        )
        self.exit_path2 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.Dropout(p=0.2),
            nn.Linear(1600, 10),
        )
        self.exit_path3 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.Dropout(p=0.2),
            nn.Linear(1152, 10),
        )
        self.exit_path4 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Flatten(),
            nn.Dropout(p=0.2),
            nn.Linear(1024, 10),
        )
        self.prob = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.conv_block1(x)
        x_exit1 = self.exit_path1(x)
        x = self.conv_block2(x)
        x_exit2 = self.exit_path2(x)
        x = self.conv_block3(x)
        x_exit3 = self.exit_path3(x)
        x = self.conv_block4(x)
        x_exit4 = self.exit_path4(x)
        return x_exit1, x_exit2, x_exit3, x_exit4

    def forward_inference(self, x):
        logit1, logit2, logit3, logit4 = self.forward(x)
        return self.prob(logit1), self.prob(logit2), self.prob(logit3),\
            self.prob(logit4)


#################################### Test ######################################


def test():
    m = model()
    print(m)
    x = torch.rand(8, 3, 32, 32)
    y1, y2, y3, y4 = m.forward_inference(x)
    print(y1.size())
    print(y2.size())
    print(y3.size())
    print(y4.size())


if __name__ == "__main__":
    test()
