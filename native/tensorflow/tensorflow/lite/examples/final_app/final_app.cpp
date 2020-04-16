/*
 * The purpose of this program is to run inference on a chosen model. The 
 * inference is done N number of times (provided as argument). This program
 * spawn a seperate thread to record the cpu load. Different load tracking
 * algorithms (smoothing by averaging, smoothing by exponentinal averaging)
 * are used, along with raw load tracking. These loads will be written in
 * global vector variable. One the inference (N number of times) is finished,
 * these loads (time stamped) is written out as a file. Along with it, another
 * file is written which shows inference runtime (which is also time-stamped).
 * 
 * This program has to be cross-compiled to work with arm64 devices.
 * /

/* Normal includes */
#include <stdlib.h>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <assert.h>
#include <iostream>
#include <vector>
#include <string>

/* included for stream */
#include <fstream>
#include <sstream>

/* includes for thread */
#include <thread>
#include <future>
#include <chrono>
#include <mutex>

/* include for tflite */
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/optional_debug_tools.h"

using namespace std;
using namespace tflite;

using Clock = chrono::high_resolution_clock;

/************************* Defines and constants ******************************/

#define TFLITE_MINIMAL_CHECK(x)                              \
  if (!(x)) {                                                \
    fprintf(stderr, "Error at %s:%d\n", __FILE__, __LINE__); \
    exit(1);                                                 \
  }

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
vector<float> loads;
vector<float> loads_average;
vector<float> loads_exponential;
vector<time_t> time_stamps;
vector<time_t> runtimes;
vector<time_t> runtime_time_stamps;

vector<float> get_snapshot(){
    ifstream stat_file("/proc/stat");
    string line, temp;
    vector<int> cpu_stat(10);
    vector<float> snapshot(3);

    while(getline(stat_file, line)){
        if(!line.compare(0, 3, "cpu")){
            istringstream ss(line);
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
    vector<float> snap1 = get_snapshot();
    this_thread::sleep_for(chrono::milliseconds(sampling_freq));
    vector<float> snap2 = get_snapshot();
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

void load_tracker(mutex& i_mutex, future<void> futureObj){
    float load;
    while(futureObj.wait_for(
                chrono::milliseconds(1)) == future_status::timeout){
        load = get_cpu_load(100);
        loads.push_back(load);
        loads_average.push_back(compute_average());
        loads_exponential.push_back(compute_exponential());
        time_stamps.push_back(Clock::now().time_since_epoch().count());
        this_thread::sleep_for(chrono::milliseconds(100));
    }
    // TODO: Some clean up work
}

int main(int argc, char* argv[]){
    /* Description for the arguments provided to the program */
    // Arg 1: model name. Eg. mobile_net.tflite
    // Arg 2: number if inference runs. Eg. 100
    if(argc != 3) {
        fprintf(stderr, "final_app <tflite_model> <nr_runs>\n");
        return 1;
    }
    const char* filename = argv[1];
    istringstream iss(argv[2]);
    int nr_runs;
    iss >> nr_runs;
    cout << filename << " " << nr_runs << endl;
    // cout << "Debug 1" << endl;
    unique_ptr<tflite::FlatBufferModel> model =
        tflite::FlatBufferModel::BuildFromFile(filename);
    TFLITE_MINIMAL_CHECK(model != nullptr);

    tflite::ops::builtin::BuiltinOpResolver resolver;
    InterpreterBuilder builder(*model, resolver);
    unique_ptr<Interpreter> interpreter;
    builder(&interpreter);
    TFLITE_MINIMAL_CHECK(interpreter != nullptr);

    TFLITE_MINIMAL_CHECK(interpreter->AllocateTensors() == kTfLiteOk);

    vector<int> inputs = interpreter->inputs();
    vector<int> outputs = interpreter->outputs();

    // for(int i=0;i<inputs.size();i++){
    //     cout << inputs[i] << " ";
    // }

    int input_index = interpreter->inputs()[0];
    TfLiteIntArray* dims = interpreter->tensor(input_index)->dims;
    // cout << "Debug 2" << endl;
    int image_height = dims->data[1];
    int image_width = dims->data[2];
    int image_channel = dims->data[3];

    int number_of_pixels = image_height * image_width * image_channel;

    /* Before starting the inference, start the load tracking thread */
    mutex i_mutex;
    promise<void> exitSignal;
    future<void> futureObj = exitSignal.get_future();
    thread t1(load_tracker, std::ref(i_mutex), std::move(futureObj));

    /* Start the inference in a loop */
    auto start = chrono::steady_clock::now();
    auto end = chrono::steady_clock::now();
    int diff;
    // cout << "Debug 3" << endl;
    for(int i=0; i<nr_runs; i++){
        auto input = interpreter->typed_tensor<float>(input_index);
        for(int j = 0; j < number_of_pixels; j++) {
            input[j] = 1;
        }
        //cout << "Debug 4" << endl;
        start = chrono::steady_clock::now();
        TFLITE_MINIMAL_CHECK(interpreter->Invoke() == kTfLiteOk);
        end = chrono::steady_clock::now();
        diff = chrono::duration_cast<chrono::milliseconds>(end - start).count();
        runtimes.push_back(diff);
        runtime_time_stamps.push_back(Clock::now().time_since_epoch().count());
    }

    /* stop the load tracking process */
    exitSignal.set_value();
    t1.join();

    /* output the data in two files */
    for(int i = 0;i<loads.size();i++){
        cout << time_stamps[i] << " " << loads_average[i] << " " << 
                        loads_exponential[i] << " " << loads[i] << endl;
    }
    for(int i=0; i<runtimes.size(); i++){
        cout << runtime_time_stamps[i] << " " << runtimes[i] << endl;
    }

    return 0;
}