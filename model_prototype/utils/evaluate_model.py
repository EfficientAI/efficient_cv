import os
# import sys
import random
import numpy as np

import torch
from torch.utils.data import DataLoader

from utils import stringify
# from plot_utils import *

# sys.path.append(os.path.abspath('.'))

from model.default import model as model_def
from dataset.default import dataset

is_cuda = torch.cuda.is_available()
device = torch.device("cuda" if is_cuda else "cpu")

torch.manual_seed(42)
torch.cuda.manual_seed(42)
random.seed(42)
np.random.seed(42)


def main():
    # #params:
    config = {'learning_rate': 0.0001,
              'nr_epochs': 500,
              'batch_size': 8}
    batch_size = 1
    model_name = stringify(["model_"] +
                           [str(k)+'_'+str(config[k]) for k in config
                            if type(config[k]) == int or
                            type(config[k]) == float])+'.pt'
    model_path = ''
    # data_path = ''
    
    # train_dataset = dataset()
    # train_loader = DataLoader(train_dataset, batch_size=batch_size,
    #                           shuffle=True)
    test_dataset = dataset()
    val_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    model_inference = model_def()
    model_inference.load_state_dict(torch.load(
                   os.path.join(model_path, model_name), map_location=device))
    model_inference.eval()

    labels = np.array([])
    outputs = np.array([])
    for batch_idx, (data, target) in enumerate(val_loader):
        prob = model_inference.forward_inference(data)
        labels = np.append(labels, target.data.to('cpu'))
        outputs = np.append(outputs, prob.data.to('cpu'))
    print(labels)
    print(outputs)


if __name__ == "__main__":
    main()
