import os
import sys
import time
from threading import Thread as thread
import subprocess

# from matplotlib import pyplot as plt
def run_interaction_process():
    monkey_runner_path = '/home/vishal/Android/Sdk/tools/bin/monkeyrunner'
    event_path = 'activity.py'
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

def main():
    # Run the program through adb

    # While the output is not produced in adb directory,
    # Repeat the automated sequence
    stop_condition = False
    runner = screen_interaction_runner()
    t = thread(target = runner.run)
    t.start()
    print("Activity has started")
    time.sleep(20)
    print("Now stopping the interaction")
    runner.terminate()
    t.join()
    # Copy the data, make the plots

    # Calculate mean and variance

    # Compute more statistics with 99th percentile and 95th percentile

if __name__ == "__main__":
    main()