#include <iostream>
#include <fstream>
#include <sstream>

#include <vector>

#include <thread>
#include <mutex>
#include <chrono>
#include <stdlib.h>

using Clock = std::chrono::high_resolution_clock;

enum CPUStates
{
	S_USER = 0,
	S_NICE,
	S_SYSTEM,
	S_IDLE,
	S_IOWAIT,
	S_IRQ,
	S_SOFTIRQ,
	S_STEAL,
	S_GUEST,
	S_GUEST_NICE
};

enum STATE
{
    ACTIVE = 0,
    IDLE,
    TOTAL
};

const int NUM_CPU_STATES = 10;
std::vector<float> loads;
std::vector<float> loads_average;
std::vector<float> loads_exponential;
std::vector<time_t> time_stamps;


std::vector<float> get_snapshot(){
    std::ifstream stat_file("/proc/stat");
    std::string line, temp;
    std::vector<int> cpu_stat(10);
    std::vector<float> snapshot(3);

    while(std::getline(stat_file, line)){
        if(!line.compare(0, 3, "cpu")){
            std::istringstream ss(line);
            ss >> temp;
            for(int i=0; i < NUM_CPU_STATES; i++){
                ss >> cpu_stat[i];
            }
        }
        break;
    }
    snapshot[ACTIVE] = static_cast<float>(cpu_stat[S_USER] +
                                     cpu_stat[S_NICE] +
                                     cpu_stat[S_SYSTEM] +
                                     cpu_stat[S_IRQ] +
                                     cpu_stat[S_SOFTIRQ] +
                                     cpu_stat[S_STEAL] +
                                     cpu_stat[S_GUEST] +
                                     cpu_stat[S_GUEST_NICE]);
    snapshot[IDLE] = static_cast<float>(cpu_stat[S_IDLE] +
                                   cpu_stat[S_IOWAIT]);
    snapshot[TOTAL] = snapshot[ACTIVE] + snapshot[IDLE];
    return snapshot;
}

float get_cpu_load(int sampling_freq){
    // sampling freq is in milliseonds, typically set to 100 ms
    // two snapshots will be taken in this internal to get diff
    std::vector<float> snap1 = get_snapshot();
    std::this_thread::sleep_for(std::chrono::milliseconds(sampling_freq));
    std::vector<float> snap2 = get_snapshot();
    return (snap2[ACTIVE] - snap1[ACTIVE])/(snap2[TOTAL] - snap1[TOTAL]);
}

float compute_average(){
    float sum = 0.0;
    int window_size = 5;
    if(loads.size() <= window_size){
        return loads[loads.size()-1];
    }
    for(int i=loads.size()-1; i>=loads.size()-window_size ;i--){
        sum = sum + loads[i];
    }
    return sum/(float)window_size;
}

float compute_exponential(){
    float val = loads[loads.size()-1];
    float factor = 0.7;
    if(loads_exponential.size() == 0){
        return val;
    }
    else{
        val = val*factor + 
              loads_exponential[loads_exponential.size()-1]*(1-factor);
        return val;
    }
}

void load_tracker(std::mutex& i_mutex){
    float load;
    for(int i=0; i<100; i++){
        load = get_cpu_load(100);
        loads.push_back(load);
        loads_average.push_back(compute_average());
        loads_exponential.push_back(compute_exponential());
        time_stamps.push_back(Clock::now().time_since_epoch().count());
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}



int main(){
    std::mutex i_mutex;
    std::thread t1(load_tracker, std::ref(i_mutex));
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    std::lock_guard<std::mutex> lock(i_mutex);
    //std::cout << loads.size() << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    //std::cout << loads.size() << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    //std::cout << loads.size() << std::endl;
    t1.join();
    // Dumpt the load data
    //for(int i = 0;i<loads.size();i++){
    //    std::cout << time_stamps[i] << " " << loads[i] << " " << loads_average[i] << " " << loads_exponential[i] << std::endl;
    //}
    for(int i = 0;i<loads.size();i++){
        std::cout << time_stamps[i] << " " << loads_average[i] << " " << loads_exponential[i] << " " << loads[i] << std::endl;
    }

    return 0;
}