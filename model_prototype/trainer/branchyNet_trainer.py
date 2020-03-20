import os
import sys
import random
import numpy as np

import torch
import torch.nn as nn
from torch import optim

from torch.utils.data import DataLoader

# sys.path.append(os.path.abspath('.'))
from utils.utils import stringify

is_cuda = torch.cuda.is_available()
device = torch.device("cuda" if is_cuda else "cpu")

torch.manual_seed(42)
torch.cuda.manual_seed(42)
random.seed(42)
np.random.seed(42)


def train_epoch(epoch, model, train_loader, optimizer, criterion,
                weights=[1.0, 0.8, 0.6, 0.5], verbose=False):
    model.train()
    epoch_loss = 0
    for batch_idx, data in enumerate(train_loader, start=0):
        img, label = data
        optimizer.zero_grad()
        o1, o2, o3, o4 = model(img)
        loss = weights[0]*criterion(o1, label) + \
            weights[1]*criterion(o2, label) + \
            weights[2]*criterion(o3, label) + \
            weights[3]*criterion(o4, label)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    if verbose:
        print('Epoch {}, Train Loss {}'.format(epoch, loss.cpu().data.numpy()))
    return epoch_loss/(batch_idx+1)


def evaluate_epoch(epoch, model, val_loader, criterion,
                   weights=[1.0, 0.8, 0.6, 0.5], verbose=False):
    model.eval()
    epoch_loss = 0
    with torch.no_grad():
        for batch_idx, data in enumerate(val_loader, start=0):
            img, label = data
            o1, o2, o3, o4 = model(img)
            loss = weights[0]*criterion(o1, label) + \
                weights[1]*criterion(o2, label) + \
                weights[2]*criterion(o3, label) + \
                weights[3]*criterion(o4, label)
            epoch_loss += loss.item()
        if verbose:
            print('Epoch {},Eval Loss {}'.format(epoch,
                                                 loss.cpu().data.numpy()))
        return epoch_loss/(batch_idx+1)


def calculate_accuracy(model, val_loader):
    corrects = [0.0]*4
    total = 0
    model.eval()
    with torch.no_grad():
        for batch_idx, data in enumerate(val_loader, start=0):
            img, label = data
            o1, o2, o3, o4 = model(img)
            outputs = [o1, o2, o3, o4]
            for i, output in enumerate(outputs):
                _, predicted = torch.max(output.data, 1)
                corrects[i] += (predicted == label).sum().item()
            total += label.size(0)
        corrects = np.array(corrects)
        return (corrects*100)/float(total)


def train(config, model_def, dataset, experiment):
    print("Device selected: ", device)
    # data_path = '/mnt/nfs/scratch1/vkeshav/vision/dataset'
    data_path = 'temp/dataset'
    # model_path = '/mnt/nfs/scratch1/vkeshav/vision/saved_models'
    model_path = 'temp/saved_models'

    learning_rate = config['learning_rate']
    nr_epochs = config['nr_epochs']
    batch_size = config['batch_size']

    print(stringify([str(k)+'_'+str(config[k]) for k in config]))
    train_dataset = dataset(data_path, split='train')
    train_loader = DataLoader(train_dataset, batch_size=batch_size,
                              shuffle=True)
    test_dataset = dataset(data_path, split='test')
    test_loader = DataLoader(test_dataset, batch_size=batch_size,
                             shuffle=False)

    model_inference = model_def()
    model_inference = model_inference.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model_inference.parameters(), lr=learning_rate)

    for epoch in range(nr_epochs+1):
        epoch_loss = train_epoch(epoch, model_inference, train_loader,
                                 optimizer, criterion, verbose=False)
        if experiment is not None:
            experiment.log_metric(stringify(["train_loss_"] +
                                  [str(config[k]) for k in config
                                      if type(config[k]) == int
                                  or type(config[k]) == float]),
                                  epoch_loss, epoch=epoch)
        else:
            print(stringify(["train_loss_"] +
                            [str(k)+'_'+str(config[k]) for k in config]),
                  epoch_loss)
        epoch_loss = evaluate_epoch(epoch, model_inference, test_loader,
                                    criterion, verbose=False)
        if experiment is not None:
            experiment.log_metric(stringify(["val_loss_"] +
                                  [str(config[k]) for k in config
                                      if type(config[k]) == int
                                  or type(config[k]) == float]), epoch_loss)
        else:
            print(stringify(["test_loss_"] +
                            [str(k)+'_'+str(config[k]) for k in config]),
                  epoch_loss)
        accuracies = calculate_accuracy(model_inference, test_loader)

        if experiment is not None:
            experiment.log_metric(stringify(["accuracy_path1"] +
                                  [str(config[k]) for k in config
                                   if type(config[k]) == int
                                  or type(config[k]) == float]), accuracies[0])
            experiment.log_metric(stringify(["accuracy_path2"] +
                                  [str(config[k]) for k in config
                                   if type(config[k]) == int
                                  or type(config[k]) == float]), accuracies[1])
            experiment.log_metric(stringify(["accuracy_path3"] +
                                  [str(config[k]) for k in config
                                   if type(config[k]) == int
                                  or type(config[k]) == float]), accuracies[2])
            experiment.log_metric(stringify(["accuracy_path4"] +
                                  [str(config[k]) for k in config
                                   if type(config[k]) == int
                                  or type(config[k]) == float]), accuracies[3])
        else:
            print(stringify(["accuracy"] +
                            [str(k)+'_'+str(config[k]) for k in config]),
                  np.mean(accuracies))
    torch.save(model_inference.state_dict(), os.path.join(model_path,
               stringify(["model_"] + [str(k)+'_'+str(config[k])
                         for k in config if type(config[k]) == int
                         or type(config[k]) == float])+'.pt'))
    print("Model written to disc")

# #################################### Test ###################################


def test():
    config = {'learning_rate': 0.001,
              'nr_epochs': 1000,
              'batch_size': 8}
    sys.path.append(os.path.abspath('.'))
    from model.default import model as model_def
    from dataset.default import dataset
    experiment = None
    train(config, model_def, dataset, experiment)


if __name__ == "__main__":
    test()
