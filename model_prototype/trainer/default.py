import os
import sys
import random
import numpy as np
import time

import torch
# import torch.nn as nn
# from torch.nn import functional as F
# from torch.autograd import Variable
# from torch import optim

# from torch.utils.data import DataLoader

sys.path.append(os.path.abspath('.'))
# from utils.utils import stringify
# from utils.utils import hit_refresh

is_cuda = torch.cuda.is_available()
device = torch.device("cuda" if is_cuda else "cpu")

torch.manual_seed(42)
torch.cuda.manual_seed(42)
random.seed(42)
np.random.seed(42)


def train_epoch(epoch, model, train_loader, optimizer, criterion,
                verbose=False):
    print("Fake Training for epoch ", epoch)
    time.sleep(10)
    return 0


def evaluate_epoch(epoch, model, val_loader, criterion, verbose=False):
    print("Fake Evaluating for epoch ", epoch)
    time.sleep(8)
    return 0


def train(config, model_def, dataset, experiment):
    pass

# #################################### Test ###################################


def test():
    pass


if __name__ == "__main__":
    test()
