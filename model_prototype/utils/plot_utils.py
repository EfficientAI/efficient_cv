# import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection


def plot_data(data, graph_labels, plot_path):
    """
    Take nd array data, graph_labels (list is plot name) and path to
    produce plot pdf
    """
    nr_data, nr_features = data.shape[0], data.shape[1]
    fig, ax = plt.subplots(nrows=nr_features, ncols=1,
                           figsize=(5 * nr_features, 10), squeeze=False)
    for i in range(nr_features):
        ax[i][0].plot(np.linspace(0, nr_data-1, nr_data), data[:, i])
        ax[i][0].set_title(graph_labels[i])
    plt.savefig(plot_path)


def plot_data_labeled(data, graph_labels, plot_path, label, pos_label=2.0):
    """
    Take nd array data, graph_labels (list is plot name) and path to
    produce plot pdf. Colors the label's pos_label with red (rest in green).
    """
    nr_data, nr_features = data.shape[0], data.shape[1]
    fig, ax = plt.subplots(nrows=nr_features, ncols=1,
                           figsize=(10, 5 * nr_features), squeeze=False)
    for i in range(nr_features):
        c = ['r' if e == pos_label else 'g' for e in label]
        x = np.linspace(0, nr_data-1, nr_data)
        y = data[:, i]
        lines = [((x0, y0), (x1, y1)) for x0, y0, x1, y1 in
                 zip(x[:-1], y[:-1], x[1:], y[1:])]
        colored_lines = LineCollection(lines, colors=c, linewidths=(2,))
        ax[i][0].add_collection(colored_lines)
        ax[i][0].set_title(graph_labels[i])
        ax[i][0].autoscale_view()
    plt.savefig(plot_path)


def plot_distribution(data, graph_labels, bins, plot_path):
    """
    takes a stream of data, can have multiple features
    Plot the distributions for the scaler values
    If there are multiple features, it plots multiple graphs.
    """
    _, nr_features = data.shape[0], data.shape[1]
    fig, ax = plt.subplots(nrows=nr_features, ncols=1,
                           figsize=(10, 10 * nr_features), squeeze=False)
    for i in range(nr_features):
        y = data[:, i]
        ax[i][0].set_title(graph_labels[i])
        ax[i][0].hist(y, color='blue', edgecolor='black', bins=bins)
    plt.savefig(plot_path)


# ################################### Test ####################################


def test_plot_data():
    a = np.random.multivariate_normal(mean=[12, 3], cov=[[2, 0], [0, 5]],
                                      size=100)
    plot_path = '/home/vishal/test/test.pdf'
    plot_data(a, ['d1', 'd2'], plot_path)


def test_plot_data_labeled():
    plot_path = '/home/vishal/test/test.pdf'
    n = 30
    _ = np.arange(n+1)
    y = np.random.randn(n+1, 1)
    print(y.shape)
    annotation = [1.0, 0.0] * 15
    plot_data_labeled(y, ['graph'], plot_path, annotation)


if __name__ == "__main__":
    pass
