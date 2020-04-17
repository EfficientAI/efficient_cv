import numpy as np
from matplotlib import pyplot as plt

def exit_point_selection(cpu_load, cpu_load_bounds, runtime_ranges,
                         accuracies, alpha):
    """
    Args:
        cpu_load: predicted cpu load
        cpu_load_bounds: a list with two elements (lower, upper)
        runtime_ranges: list of tuple of size equal to number of exit points
        accuracies: list of size equal to number of exit points
        alpha: float in range 0 to 1 for QoS
    
    Returns:
        index of the choses exit point, predicted_runtime
    """
    predicted_runtimes = []
    runtime_penalty = []
    accuracy_penalty = []
    cpu_load_lower, cpu_load_upper = cpu_load_bounds
    for _, runtime_bound in enumerate(runtime_ranges):
        (runtime_lower, runtime_upper) = runtime_bound
        increment_scale = float(runtime_upper - runtime_lower)
        increment_scale = increment_scale/(cpu_load_upper - cpu_load_lower)
        increment_scale = int(increment_scale*cpu_load)
        predicted_runtime = runtime_lower + increment_scale
        predicted_runtimes.append(predicted_runtime)
    ideal_runtime = runtime_ranges[-1][0]
    ideal_accuracy = accuracies[-1]
    for index, predicted_run in enumerate(predicted_runtimes):
        runtime_penalty.append(predicted_run - ideal_runtime)
        accuracy_penalty.append(ideal_accuracy - accuracies[index])
    runtime_penalty = np.array(runtime_penalty)
    runtime_normalized = (runtime_penalty - min(runtime_penalty))/ \
                         (max(runtime_penalty) - min(runtime_penalty))
    accuracy_penalty = np.array(accuracy_penalty)
    accuracy_normalized = (accuracy_penalty - min(accuracy_penalty))/ \
                          (max(accuracy_penalty) - min(accuracy_penalty))
    total_penalty = alpha*runtime_normalized + (1-alpha)*accuracy_normalized
    return np.argmin(total_penalty), predicted_runtimes


def main():
    (load_timestamp, avg_loads, exp_loads, raw_loads,
            runtime_timestamps, runtimes) = (np.load("load_timestamp.npy"),
            np.load("avg_loads.npy"), np.load("exp_loads.npy"),
            np.load("raw_loads.npy"), np.load("runtime_timestamps.npy"),
            np.load("runtimes.npy"))
    cpu_load_bounds = (0.2, 0.9)
    runtime_ranges = [(20, 40), (30, 55), (50, 110), (70, 140), (110, 210), (140, 230)]
    accuracies = [60.3, 65.4, 69.8, 71.8, 74.4, 75.0]
    alpha = 0.33
    predicted_runtime = []
    indexes = []
    for index, real_runtime in enumerate(runtimes):
        time_stamp = runtime_timestamps[index]
        cpu_load = avg_loads[np.abs(load_timestamp - time_stamp).argmin()]
        out_index, predicted = exit_point_selection(cpu_load, cpu_load_bounds,
                                                    runtime_ranges,
                                                    accuracies, alpha)
        indexes.append(out_index)
        predicted_runtime.append(predicted[-1])
    predicted_runtime = np.array(predicted_runtime)
    indexes = np.array(indexes)
    # print(indexes)

    # plt.plot(load_timestamp, avg_loads, label='avg_loads')
    # plt.plot(load_timestamp, exp_loads, label='exp_loads')
    # plt.plot(load_timestamp, raw_loads, label='instant_loads')

    nr_evict_data = int(0.05*float(len(runtimes)))
    evict_indices = np.argpartition(runtimes, -nr_evict_data)[-nr_evict_data:]
    new_runtime_timestamps = np.delete(runtime_timestamps, evict_indices)
    new_runtimes = np.delete(runtimes, evict_indices)
    till = int((5/8)*len(new_runtimes))
    till = -1
    new_runtimes = new_runtimes[:till]

    new_predicted_runtimes = np.delete(predicted_runtime, evict_indices)
    new_predicted_runtimes = new_predicted_runtimes[:till]

    new_runtime_timestamps = new_runtime_timestamps[:till]

    plt.plot(new_runtime_timestamps, new_runtimes,
             label='runtimes', marker='o')
    plt.plot(new_runtime_timestamps, new_predicted_runtimes,
             label='predicted_runtimes', marker='x')
    plt.legend(loc="upper right")
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()


def test():
    cpu_load = 0.9
    cpu_load_bounds = (0.2, 0.9)
    runtime_ranges = [(20, 40), (30, 55), (50, 110), (70, 140), (110, 210), (140, 230)]
    accuracies = [60.3, 65.4, 69.8, 71.8, 74.4, 75.0]
    alpha = 0.40
    idx, r = exit_point_selection(cpu_load, cpu_load_bounds, runtime_ranges,
                                  accuracies, alpha)
    print(r)
    print(idx)


if __name__ == "__main__":
    #main()
    test()

