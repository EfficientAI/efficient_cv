import os
import sys
# import numpy as np

import torch
import torch.nn as nn
# from torch.autograd import Variable

sys.path.append(os.path.abspath('.'))
# from utils.utils import stringify


is_cuda = torch.cuda.is_available()
device = torch.device("cuda" if is_cuda else "cpu")


class model(nn.Module):
    def __init__(self):
        super(model, self).__init__()
        pass

    def forward(self, x):
        return

    def forward_inference(self, x):
        return


# ################################### Test ####################################


def test():
    m = model()
    print(m)


if __name__ == "__main__":
    test()
