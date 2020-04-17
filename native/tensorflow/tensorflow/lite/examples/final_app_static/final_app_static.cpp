/*
 * The purpose of this program is to run inference on several model. The 
 * inference is done N number of times (provided as argument). Each time, cpu
 * load is analyzed and a model with best accuracy-runtime characteristics
 * is selected. The selected model serves as best runtime use-case.This program
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


/*************************** Utility functions *******************************/

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

vector<float> normalize_data(vector<float> &data){
    vector<float> ret;
    float min_data = data[0], max_data = data[0];
    for(float d : data){
        if(d < min_data){
            min_data = d;
        }
        if(d > max_data){
            max_data = d;
        }
    }
    for(float d : data){
        ret.push_back((d - min_data)/(max_data - min_data));
    }
    return ret;
}

int exit_point_selection(float cpu_load, pair<float, float> &cpu_load_bound,
    vector<pair<int, int> > &runtime_ranges, vector<float> &accuracies, 
    float alpha){
    /*
     * Follows same argument type as that of python definition
    */
    vector<int> predicted_runtimes;
    vector<float> runtime_penalty;
    vector<float> accuracy_penalty;

    int runtime_lower, runtime_upper, increment_scale;
    int predicted_runtime;
    float total_penalty, min_penalty, best_index;
    min_penalty = 1;
    best_index = 0;

    float cpu_load_lower = cpu_load_bound.first;
    float cpu_load_upper = cpu_load_bound.second;
    for(pair<int, int> runtime_bound : runtime_ranges){
        runtime_lower = runtime_bound.first;
        runtime_upper = runtime_bound.second;
        increment_scale = (float)(runtime_upper - runtime_lower);
        increment_scale = increment_scale/(cpu_load_upper - cpu_load_lower);
        increment_scale = (int)(increment_scale*cpu_load);
        predicted_runtime = runtime_lower + increment_scale;
        predicted_runtimes.push_back(predicted_runtime);
    }
    int ideal_runtime = runtime_ranges[runtime_ranges.size()-1].first;
    float ideal_accuracy = accuracies[accuracies.size()-1];
    for(int index = 0; index<predicted_runtimes.size(); index++){
        int predicted_run = predicted_runtimes[index];
        runtime_penalty.push_back(predicted_run - ideal_runtime);
        accuracy_penalty.push_back(ideal_accuracy - accuracies[index]);
    }
    vector<float> runtime_normalized = normalize_data(runtime_penalty);
    vector<float> accuracy_normalized = normalize_data(accuracy_penalty);
    for(int index=0; index<runtime_normalized.size(); index++){
        total_penalty = alpha*runtime_normalized[index] + 
                            (1.0 - alpha)*accuracy_normalized[index];
        if(total_penalty < min_penalty){
            min_penalty = total_penalty;
            best_index = index;
        }
    }
    return best_index;
}


int main(int argc, char* argv[]){
    /* Description for the arguments provided to the program */
    // Arg 1: number if inference runs. Eg. 100
    // cout << "Debug 0" << endl;
    if(argc != 2) {
        fprintf(stderr, "final_app <tflite_model> <nr_runs>\n");
        return 1;
    }
    // Constants for the 6 models we are using
    pair<float, float> cpu_load_bound = make_pair(0.2, 0.9);
    vector<pair<int, int> > runtime_ranges = {{20, 40}, {30, 55}, {50, 110},
                                            {70, 140}, {110, 210}, {140, 230}};
    vector<float> accuracies = {60.3, 65.4, 69.8, 71.8, 74.4, 75.0};
    float alpha = 0.33;
    // cout << "Debug 0.5" << endl;
    istringstream iss(argv[1]);
    int nr_runs;
    iss >> nr_runs;
    cout << nr_runs << endl;
    // cout << "Debug 1" << endl;
    unique_ptr<tflite::FlatBufferModel> model1 =
        tflite::FlatBufferModel::BuildFromFile("/data/local/tmp/"
                                               "final_app_static/"
                                               "mobilenet2_6.tflite");
    TFLITE_MINIMAL_CHECK(model1 != nullptr);

    unique_ptr<tflite::FlatBufferModel> model2 =
        tflite::FlatBufferModel::BuildFromFile("/data/local/tmp/"
                                               "final_app_static/"
                                               "mobilenet2_5.tflite");
    TFLITE_MINIMAL_CHECK(model2 != nullptr);

    unique_ptr<tflite::FlatBufferModel> model3 =
        tflite::FlatBufferModel::BuildFromFile("/data/local/tmp/"
                                               "final_app_static/"
                                               "mobilenet2_4.tflite");
    TFLITE_MINIMAL_CHECK(model3 != nullptr);

    unique_ptr<tflite::FlatBufferModel> model4 =
        tflite::FlatBufferModel::BuildFromFile("/data/local/tmp/"
                                               "final_app_static/"
                                               "mobilenet2_3.tflite");
    TFLITE_MINIMAL_CHECK(model4 != nullptr);

    unique_ptr<tflite::FlatBufferModel> model5 =
        tflite::FlatBufferModel::BuildFromFile("/data/local/tmp/"
                                               "final_app_static/"
                                                "mobilenet2_2.tflite");
    TFLITE_MINIMAL_CHECK(model5 != nullptr);

    unique_ptr<tflite::FlatBufferModel> model6 =
        tflite::FlatBufferModel::BuildFromFile("/data/local/tmp/"
                                               "final_app_static/"
                                               "mobilenet2_1.tflite");
    TFLITE_MINIMAL_CHECK(model6 != nullptr);

    // cout << "Debug 1.5" << endl;

    tflite::ops::builtin::BuiltinOpResolver resolver1;
    tflite::ops::builtin::BuiltinOpResolver resolver2;
    tflite::ops::builtin::BuiltinOpResolver resolver3;
    tflite::ops::builtin::BuiltinOpResolver resolver4;
    tflite::ops::builtin::BuiltinOpResolver resolver5;
    tflite::ops::builtin::BuiltinOpResolver resolver6;

    InterpreterBuilder builder1(*model1, resolver1);
    unique_ptr<Interpreter> interpreter1;
    builder1(&interpreter1);
    TFLITE_MINIMAL_CHECK(interpreter1 != nullptr);

    TFLITE_MINIMAL_CHECK(interpreter1->AllocateTensors() == kTfLiteOk);

    InterpreterBuilder builder2(*model2, resolver2);
    unique_ptr<Interpreter> interpreter2;
    builder2(&interpreter2);
    TFLITE_MINIMAL_CHECK(interpreter2 != nullptr);

    TFLITE_MINIMAL_CHECK(interpreter2->AllocateTensors() == kTfLiteOk);

    InterpreterBuilder builder3(*model3, resolver3);
    unique_ptr<Interpreter> interpreter3;
    builder3(&interpreter3);
    TFLITE_MINIMAL_CHECK(interpreter3 != nullptr);

    TFLITE_MINIMAL_CHECK(interpreter3->AllocateTensors() == kTfLiteOk);

    InterpreterBuilder builder4(*model4, resolver4);
    unique_ptr<Interpreter> interpreter4;
    builder4(&interpreter4);
    TFLITE_MINIMAL_CHECK(interpreter4 != nullptr);

    TFLITE_MINIMAL_CHECK(interpreter4->AllocateTensors() == kTfLiteOk);

    InterpreterBuilder builder5(*model5, resolver5);
    unique_ptr<Interpreter> interpreter5;
    builder5(&interpreter5);
    TFLITE_MINIMAL_CHECK(interpreter5 != nullptr);

    TFLITE_MINIMAL_CHECK(interpreter5->AllocateTensors() == kTfLiteOk);

    InterpreterBuilder builder6(*model6, resolver6);
    unique_ptr<Interpreter> interpreter6;
    builder6(&interpreter6);
    TFLITE_MINIMAL_CHECK(interpreter6 != nullptr);

    TFLITE_MINIMAL_CHECK(interpreter6->AllocateTensors() == kTfLiteOk);

    vector<int> inputs = interpreter1->inputs();
    vector<int> outputs = interpreter1->outputs();

    // for(int i=0;i<inputs.size();i++){
    //     cout << inputs[i] << " ";
    // }

    int input_index1 = interpreter1->inputs()[0];
    int input_index2 = interpreter2->inputs()[0];
    int input_index3 = interpreter3->inputs()[0];
    int input_index4 = interpreter4->inputs()[0];
    int input_index5 = interpreter5->inputs()[0];
    int input_index6 = interpreter6->inputs()[0];

    TfLiteIntArray* dims = interpreter1->tensor(input_index1)->dims;
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
        auto input = interpreter1->typed_tensor<float>(input_index1);
        for(int j = 0; j < number_of_pixels; j++) {
            input[j] = 1;
        }
        // cout << "Debug 3.5" << endl;
        input = interpreter2->typed_tensor<float>(input_index2);
        for(int j = 0; j < number_of_pixels; j++) {
            input[j] = 1;
        }
        // cout << "Debug 3.6" << endl;
        input = interpreter3->typed_tensor<float>(input_index3);
        for(int j = 0; j < number_of_pixels; j++) {
            input[j] = 1;
        }
        input = interpreter4->typed_tensor<float>(input_index4);
        for(int j = 0; j < number_of_pixels; j++) {
            input[j] = 1;
        }
        input = interpreter5->typed_tensor<float>(input_index5);
        for(int j = 0; j < number_of_pixels; j++) {
            input[j] = 1;
        }
        input = interpreter6->typed_tensor<float>(input_index6);
        for(int j = 0; j < number_of_pixels; j++) {
            input[j] = 1;
        }
        //cout << "Debug 4" << endl;
        start = chrono::steady_clock::now();
        /*
         * The logic to select the exit point is here.
         */
        // cout << "Debug 4" << endl;
        float cpu_load;
        if(loads_average.size() == 0){
            cpu_load = 0.2;
        }
        else{
            cpu_load = loads_average[loads_average.size()-1];
        }
        // cout << "Debug 5" << endl;
        //TODO: I should take  a lock before accesing cpu_load, but who cares.
        int exit_point = exit_point_selection(cpu_load, cpu_load_bound,
                                        runtime_ranges, accuracies, alpha);
        // cout << exit_point << endl;
        if(exit_point == 0){
            TFLITE_MINIMAL_CHECK(interpreter1->Invoke() == kTfLiteOk);
        }
        else if(exit_point == 1){
            TFLITE_MINIMAL_CHECK(interpreter2->Invoke() == kTfLiteOk);
        }
        else if(exit_point == 2){
            TFLITE_MINIMAL_CHECK(interpreter3->Invoke() == kTfLiteOk);
        }
        else if(exit_point == 3){
            TFLITE_MINIMAL_CHECK(interpreter4->Invoke() == kTfLiteOk);
        }
        else if(exit_point == 4){
            TFLITE_MINIMAL_CHECK(interpreter5->Invoke() == kTfLiteOk);
        }
        else{
            TFLITE_MINIMAL_CHECK(interpreter6->Invoke() == kTfLiteOk);
        }
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
