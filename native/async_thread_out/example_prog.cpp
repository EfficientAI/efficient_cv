#include <stdio.h>
#include <stdlib.h> 
#include <iostream>
#include <vector>

#include <thread>
#include <mutex>

typedef std::chrono::high_resolution_clock Clock;

using namespace std;

int global_load = 0;

int load_tracker(std::mutex& i_mutex){
    while(1){
        std::lock_guard<std::mutex> lock(i_mutex);
        global_load = global_load + 10;
        // Now sleep for some time
        this_thread::sleep_for(chrono::milliseconds(10000));
    }
}

int main(){
    std::mutex i_mutex;
    std::thread t1(load_tracker, std::ref(i_mutex));
    while(1){
        std::lock_guard<std::mutex> lock(i_mutex);
        cout << "global load now is " << global_load << endl;
        this_thread::sleep_for(chrono::milliseconds(1000));
    }
    return 0;
}