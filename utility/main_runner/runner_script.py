import os
import sys
import time
import numpy as np
from threading import Thread as thread
import subprocess

from matplotlib import pyplot as plt


def run_interaction_process():
    monkey_runner_path = '/home/vishal/Android/Sdk/tools/bin/monkeyrunner'
    event_path = '/home/vishal/Github_umass/efficient_cv/utility/main_runner/activity.py'
    out = subprocess.run([monkey_runner_path, event_path],
                         stdout=subprocess.DEVNULL)


class screen_interaction_runner:
    def __init__(self):
        self._is_running = True
    
    def terminate(self):
        self._is_running = False
    
    def run(self):
        while self._is_running:
            run_interaction_process()


def parse_encoded_out(s):
    """
    Format: lines with three characters represents
            (time_stamp, average_load, exp_load, raw_load)
            lines with two charatacters represents
            (time_stamp, runtime)
            The first line and any blank line will be discarded
    """
    load_timestamp = []
    avg_loads = []
    exp_loads = []
    raw_loads = []
    runtime_timestamps = []
    runtimes = []
    s_lines = s.splitlines()
    # print(s_lines)

    for index, line in enumerate(s_lines):
        if index == 0 or index == 1:
            continue
        if len(line) == 0:
            continue
        words = line.split()
        if len(words) == 4:
            load_timestamp.append(int(words[0]))
            avg_loads.append(float(words[1]))
            exp_loads.append(float(words[2]))
            raw_loads.append(float(words[3]))
        else:
            runtime_timestamps.append(int(words[0]))
            runtimes.append(float(words[1]))
    return (load_timestamp, avg_loads, exp_loads, raw_loads,
            runtime_timestamps, runtimes)


def get_plots(stdout):
    start_index = 5
    encoded_out = str(stdout, encoding='utf-8')
    parsed_out = parse_encoded_out(encoded_out)
    (load_timestamp, avg_loads, exp_loads, raw_loads,
            runtime_timestamps, runtimes) = parsed_out
    
    # First dump all the date, and lets worry about it layer
    np.save("load_timestamp.npy", np.array(load_timestamp))
    np.save("avg_loads.npy", np.array(avg_loads))
    np.save("exp_loads.npy", np.array(exp_loads))
    np.save("raw_loads.npy", np.array(raw_loads))
    np.save("runtime_timestamps.npy", np.array(runtime_timestamps))
    np.save("runtimes.npy", np.array(runtimes))

    plt.plot(load_timestamp[start_index:], avg_loads[start_index:],
             label='avg_loads')
    plt.plot(load_timestamp[start_index:], exp_loads[start_index:],
             label='exp_loads')
    plt.plot(load_timestamp[start_index:], raw_loads[start_index:],
             label='instant_loads')
    #plt.legend(loc="upper right")
    #plt.show()

    #plt.clf()
    #plt.cla()
    #plt.close()
    runtimes = runtimes[start_index:]
    runtimes_arr = np.array(runtimes, dtype = np.float)
    diff = np.max(runtimes_arr) - np.min(runtimes_arr)
    runtimes_scaled = list((runtimes_arr - np.min(runtimes_arr))/diff)
    # print(runtime_timestamps)
    # print(runtimes)
    # print(runtimes_scaled)
    plt.plot(runtime_timestamps[start_index:], runtimes_scaled,
             label='runtimes', marker='o')
    plt.legend(loc="upper right")
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()



def main():
    adb_command = '/home/vishal/Android/Sdk/platform-tools/adb'
    program_file = '/data/local/tmp/milestone3/final_app'
    model_file = '/data/local/tmp/milestone3/mobilenet2.tflite'
    nr_runs = 1000

    runner = screen_interaction_runner()
    t = thread(target = runner.run)
    t.start()

    time.sleep(20) # Wait

    print("Activity has started")
    out = subprocess.Popen([adb_command, 'shell', program_file, 
                            model_file, str(nr_runs)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, _ = out.communicate()
    print("Now stopping the interaction")

    try:
        get_plots(stdout)
    except Exception as err:
        print(err)
        print(stdout)
    finally:
        pass
    
    runner.terminate()
    t.join()

    # Calculate mean and variance

    # Compute more statistics with 99th percentile and 95th percentile

if __name__ == "__main__":
    main()