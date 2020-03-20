import os
import sys

import torch
# import torchvision
# import torchvision.transforms as transforms
from torch.utils.data import Dataset

sys.path.append(os.path.abspath('.'))
# from utils.utils import stringify


is_cuda = torch.cuda.is_available()
device = torch.device("cuda" if is_cuda else "cpu")


class dataset(Dataset):
    def __init__(self):
        pass

    def __getitem__(self, idx):
        return 0

    def __len__(self):
        return 100

# ################################# Test ######################################


def test():
    d = dataset()
    print(len(d))


if __name__ == "__main__":
    test()
