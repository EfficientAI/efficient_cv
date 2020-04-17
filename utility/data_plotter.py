import numpy as np
from matplotlib import pyplot as plt

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

if __name__ == "__main__":
    plot_data()