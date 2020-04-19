import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

def plot_data():
    (load_timestamp, avg_loads, exp_loads, raw_loads,
            runtime_timestamps, runtimes) = (np.load("load_timestamp.npy"),
            np.load("avg_loads.npy"), np.load("exp_loads.npy"),
            np.load("raw_loads.npy"), np.load("runtime_timestamps.npy"),
            np.load("runtimes.npy"))

    # get the 95% percentile runtime data
    nr_evict_data = int(0.05*float(len(runtimes)))
    evict_indices = np.argpartition(runtimes, -nr_evict_data)[-nr_evict_data:]
    print("Removing: ", runtimes[evict_indices])
    new_runtime_timestamps = np.delete(runtime_timestamps, evict_indices)
    new_runtimes = np.delete(runtimes, evict_indices)

    #plt.plot(load_timestamp, avg_loads, label='avg_loads')
    #plt.plot(load_timestamp, exp_loads, label='exp_loads')
    #plt.plot(load_timestamp, raw_loads, label='instant_loads')
    #plt.legend(loc="upper right")
    #plt.show()

    #plt.clf()
    #plt.cla()
    #plt.close()
    #diff = np.max(new_runtimes) - np.min(new_runtimes)
    #runtimes_scaled = list((new_runtimes - np.min(new_runtimes))/diff)
    # print(runtime_timestamps)
    # print(runtimes)
    # print(runtimes_scaled)
    plt.plot(new_runtime_timestamps, new_runtimes,
             label='runtimes', marker='o')
    plt.legend(loc="upper right")
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()

def hist_plot_data():
    all_runtimes = []
    plt.figure(figsize=(13,7))
    for i in range(1,5):
        data_path = 'mobilenet2_{}_data/runtimes.npy'.format(i)
        runtimes = np.load(data_path)
        all_runtimes.append(runtimes)
        plt.hist(runtimes, 100, alpha=0.6, label='model_{}'.format(i))
    plt.xlabel('runtime in millisecond')
    plt.ylabel('frequency of runtimes')
    plt.legend()
    plt.savefig('drawing2.pdf')

def hist_plot_data_final():
    all_runtimes = []
    plt.style.use('seaborn-white')
    plt.figure(figsize=(13,7))
    data_path = 'mobilenet2_all(0.33)_data/runtimes.npy'
    runtimes = np.load(data_path)
    all_runtimes.append(runtimes)
    plt.hist(runtimes, 100, alpha=0.8, label='alpha = 0.5')
    plt.xlabel('runtime in millisecond')
    plt.ylabel('frequency of runtimes')
    plt.legend()
    # plt.show()
    plt.savefig('drawing_final.pdf')

def compute_average_accuracy():
    all_runtimes = []
    runtime_path = 'mobilenet2_all(0.33)_data/runtimes.npy'
    # runtime_path = 'runtimes.npy'
    exit_path = 'mobilenet2_all(0.33)_data/exits.npy'
    runtimes = np.load(runtime_path)
    exits = np.load(exit_path)
    accuracies = [60.3, 65.4, 69.8, 71.8, 74.4, 75.0]
    avg_accuracy = 0.0
    for e in exits:
        avg_accuracy += accuracies[e]
    avg_accuracy /= len(exits)
    print(avg_accuracy)
    a  = []
    average_runtime = 0.0
    for r in runtimes:
        a.append(max(0.0, (r - 150.0)))
        average_runtime += r
    average_runtime /= len(runtimes)
    a = np.array(a)
    print("varaince ", np.std(a), " runtime ", average_runtime)

def plot_load_runtime():
    load_timestamp_path = 'mobilenet2_{}_data/load_timestamp.npy'.format(1)
    avg_load_path = 'mobilenet2_{}_data/avg_loads.npy'.format(1)
    exp_load_path = 'mobilenet2_{}_data/exp_loads.npy'.format(1)
    raw_load_path = 'mobilenet2_{}_data/raw_loads.npy'.format(1)
    runtime_timestamp = 'mobilenet2_{}_data/runtime_timestamps.npy'.format(1)
    runtimes = 'mobilenet2_{}_data/runtimes.npy'.format(1)
    (load_timestamp, avg_loads, exp_loads, raw_loads,
            runtime_timestamps, runtimes) = (np.load(load_timestamp_path),
            np.load(avg_load_path), np.load(exp_load_path),
            np.load(raw_load_path), np.load(runtime_timestamp),
            np.load(runtimes))

    nr_evict_data = int(0.05*float(len(runtimes)))
    evict_indices = np.argpartition(runtimes, -nr_evict_data)[-nr_evict_data:]
    print("Removing: ", runtimes[evict_indices])
    runtime_timestamps = np.delete(runtime_timestamps, evict_indices)
    runtimes = np.delete(runtimes, evict_indices)

    till = int((5/8)*len(load_timestamp))
    #till = -1
    load_timestamp = load_timestamp[:till]
    avg_loads = avg_loads[:till]
    exp_loads = exp_loads[:till]
    raw_loads = raw_loads[:till]

    till = int((5/8)*len(runtime_timestamps))
    runtime_timestamps = runtime_timestamps[:till]
    runtimes = runtimes[:till]


    plt.style.use('seaborn-white')
    fig = plt.figure(figsize=(20,10))
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    ax1.plot(load_timestamp,raw_loads, label = 'instantaneous load')
    ax1.plot(load_timestamp,exp_loads, label = 'exponential moving average')
    ax1.plot(load_timestamp,avg_loads, label = 'moving window average')

    ax2.plot(runtime_timestamps, runtimes, label='runtimes', marker='o', alpha = 0.9)

    ax1.set(xlim = (min(load_timestamp), max(load_timestamp)))
    ax1.set(xlabel = 'Timestamps')
    ax1.set(ylabel = 'cpu loads')
    ax2.set(xlim = (min(load_timestamp), max(load_timestamp)))
    ax2.set(xlabel = 'Timestamps')
    ax2.set(ylabel = 'inference time in milliseconds')

    ax1.legend(loc="lower right")
    ax2.legend(loc="upper right")
    plt.savefig('drawing3.pdf')

if __name__ == "__main__":
    # plot_data()
    # hist_plot_data()
    # plot_load_runtime()
    hist_plot_data_final()
    compute_average_accuracy()