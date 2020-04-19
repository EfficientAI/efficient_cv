import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

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
        runtime_penalty.append(max(0, predicted_run - ideal_runtime)**2)
        accuracy_penalty.append(ideal_accuracy - accuracies[index])
    runtime_penalty = np.array(runtime_penalty)
    runtime_normalized = (runtime_penalty - min(runtime_penalty))/ \
                         (max(runtime_penalty) - min(runtime_penalty))
    accuracy_penalty = np.array(accuracy_penalty)
    accuracy_normalized = (accuracy_penalty - min(accuracy_penalty))/ \
                          (max(accuracy_penalty) - min(accuracy_penalty))
    total_penalty = alpha*runtime_normalized + (1-alpha)*accuracy_normalized
    return np.argmin(total_penalty), predicted_runtimes, total_penalty[np.argmin(total_penalty)]


def main():
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
    cpu_load_bounds = (0.2, 0.9)
    runtime_ranges = [(20, 40), (30, 55), (50, 110), (70, 140), (110, 210), (140, 230)]
    accuracies = [60.3, 65.4, 69.8, 71.8, 74.4, 75.0]
    alpha = 0.33
    predicted_runtime = []
    indexes = []
    for index, real_runtime in enumerate(runtimes):
        time_stamp = runtime_timestamps[index]
        cpu_load = avg_loads[np.abs(load_timestamp - time_stamp).argmin()]
        out_index, predicted, _ = exit_point_selection(cpu_load, cpu_load_bounds,
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
    # till = -1
    new_runtimes = new_runtimes[:till]

    new_predicted_runtimes = np.delete(predicted_runtime, evict_indices)
    new_predicted_runtimes = new_predicted_runtimes[:till]

    new_runtime_timestamps = new_runtime_timestamps[:till]

    plt.figure(figsize=(20,5))

    plt.plot(new_runtime_timestamps, new_runtimes,
             label='runtimes', marker='o')
    plt.plot(new_runtime_timestamps, new_predicted_runtimes,
             label='predicted_runtimes', marker='x')
    plt.xlabel('Timestamps')
    plt.ylabel('Inference runtimes')
    plt.legend(loc="lower right")
    # plt.show()
    plt.savefig('drawing4.pdf')

    plt.clf()
    plt.cla()
    plt.close()

def parameter_effect_plot():
    cpu_loads = np.linspace(0.2, 0.9, 10)
    alphas = [0.0, 0.1, 0.7, 0.95, 1.0]
    cpu_load_bounds = (0.2, 0.9)
    runtime_ranges = [(20, 40), (30, 55), (50, 110), (70, 140), (110, 210), (140, 230)]
    accuracies = [60.3, 65.4, 69.8, 71.8, 74.4, 75.0]
    penalties = {}
    exits = {}
    colors = {0: 'red', 1: 'blue', 2: 'green', 3: 'black', 4: 'yellow', 5:'cyan'}
    sizes = {0: 10, 1: 12, 2: 14, 3: 16, 4: 18, 5: 20}
    shapes = {0: "P", 1: "h", 2: "s", 3: "X", 4: "^", 5: "o"}
    for alpha in alphas:
        d = []
        e = []
        for cpu_load in cpu_loads:
            idx, r, p = exit_point_selection(cpu_load, cpu_load_bounds, runtime_ranges,
                                  accuracies, alpha)
            d.append(p)
            e.append(idx)
        penalties[alpha] = d
        exits[alpha] = e
    print(penalties[0])
    print(exits[0])
    # Cutom legend
    legend_elements = []
    for i in range(6):
        legend_elements.append(Line2D([0], [0], marker=shapes[i], color='w', label='Model_{}'.format(i+1),
                          markerfacecolor=colors[i], markersize=15,  alpha = 0.8))
    # Now plot all data
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_subplot(111)
    for alpha in alphas:
        ax.plot(cpu_loads, penalties[alpha], label='alpha={}'.format(alpha), marker='x', markersize = 1)
    for alpha in alphas:
        for x, y, c in zip(cpu_loads, penalties[alpha], exits[alpha]):
            ax.plot(x,y, marker = shapes[c], markerfacecolor=colors[c],markeredgecolor=colors[c], markersize=sizes[c], alpha = 0.8)
    leg1 = ax.legend(loc='upper left')
    leg2 = ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.15,1.0))
    ax.add_artist(leg1)
    plt.xlabel('cpu load')
    plt.ylabel('penalty score')

    plt.savefig('drawing5.pdf')
    # plt.show()


def test():
    cpu_load = 0.5
    cpu_load_bounds = (0.2, 0.9)
    runtime_ranges = [(20, 40), (30, 55), (50, 110), (70, 140), (110, 210), (140, 230)]
    accuracies = [60.3, 65.4, 69.8, 71.8, 74.4, 75.0]
    alpha = 0.0
    idx, r, p = exit_point_selection(cpu_load, cpu_load_bounds, runtime_ranges,
                                  accuracies, alpha)
    print(r)
    print(idx)

def get_penalty_data():
    cpu_load_bounds = (0.2, 0.9)
    runtime_ranges = [(20, 40), (30, 55), (50, 110), (70, 140), (110, 210), (140, 230)]
    accuracies = [60.3, 65.4, 69.8, 71.8, 74.4, 75.0]
    for i in range(1,6):
        load_timestamp_path = 'mobilenet2_{}_data/load_timestamp.npy'.format(i)
        avg_load_path = 'mobilenet2_{}_data/avg_loads.npy'.format(i)
        exp_load_path = 'mobilenet2_{}_data/exp_loads.npy'.format(i)
        raw_load_path = 'mobilenet2_{}_data/raw_loads.npy'.format(i)
        runtime_timestamp = 'mobilenet2_{}_data/runtime_timestamps.npy'.format(i)
        runtimes = 'mobilenet2_{}_data/runtimes.npy'.format(i)
        (load_timestamp, avg_loads, exp_loads, raw_loads,
                runtime_timestamps, runtimes) = (np.load(load_timestamp_path),
                np.load(avg_load_path), np.load(exp_load_path),
                np.load(raw_load_path), np.load(runtime_timestamp),
                np.load(runtimes))
        a = []
        average_runtime = 0.0
        for r in runtimes:
            a.append(max(0.0, (r - 150.0)))
            average_runtime += r
        average_runtime /= len(runtimes)
        a = np.array(a)
        print("Model {}".format(i), " varaince ", np.std(a), " runtime ", average_runtime)
    

if __name__ == "__main__":
    # main()
    # test()
    # parameter_effect_plot()
    get_penalty_data()

