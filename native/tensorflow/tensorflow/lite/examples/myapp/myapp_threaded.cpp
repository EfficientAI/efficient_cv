#include <cstdio>
#include <cstdlib>
#include <sstream>
#include <iostream>
#include <vector>
#include <chrono>
#include <unistd.h>

#include <thread> 

#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/optional_debug_tools.h"

typedef std::chrono::high_resolution_clock Clock;

// Usage: myapp <tflite model> nr_runs
using namespace std;
using namespace tflite;

#define TFLITE_MINIMAL_CHECK(x)                              \
  if (!(x)) {                                                \
    fprintf(stderr, "Error at %s:%d\n", __FILE__, __LINE__); \
    exit(1);                                                 \
  }

void workload(int thread_time, int compute_time, int sleep_time) { 
    // Based on the load, this function does proportinal useless computation
    // more load, more the computation and less the sleeping
    int loops = (int)((thread_time)/(compute_time + sleep_time)) + 1;
    for(int i=0;i<loops;i++){
        float var = 2.0;
        auto t1 = Clock::now();
        auto wakeup = t1 + chrono::milliseconds(compute_time);
        while(Clock::now() < wakeup) {
            if(var > 1000000){
                var = 2.0;
            }
            var = var + 1.0;
            var = var*var;
        }
        this_thread::sleep_for(chrono::milliseconds(sleep_time));
    }
}

int main(int argc, char* argv[]) {
    cout << "Inputs are loop, compute_time, sleep_time, nr_threads" << endl;
    cout << "myapp_threaded program" << endl;
    if (argc != 5) {
        fprintf(stderr, "myapp <tflite model> nr_runs loop compute_time sleep_time nr_thread\n");
        return 1;
    }
    const char* filename = argv[1];
    int val;
    int thread_time;
    int compute_time;
    int sleep_time;
    int nr_thread;
    istringstream iss1(argv[2]);
    iss1 >> val;
    istringstream iss2(argv[3]);
    iss2 >> thread_time;
    istringstream iss3(argv[4]);
    iss3 >> compute_time;
    /*istringstream iss4(argv[5]);
    iss4 >> sleep_time;
    istringstream iss5(argv[6]);
    iss5 >> nr_thread;
    cout << "file received: " << filename << " nr_runs received: " << val << endl;*/
    //cout << "thread_time: " << thread_time << " compute_time: " << compute_time << " sleep_time: " << sleep_time << " nr_thread: " << nr_thread << endl;

    auto start = chrono::steady_clock::now();
    auto end = chrono::steady_clock::now();
    /*sleep(1);
    vector<thread> threads;
    for(int i=0;i<nr_thread;i++){
        thread th(workload, thread_time, compute_time, sleep_time);
        threads.push_back(std::move(th));
    }
    for(int i=0;i<nr_thread;i++){
        if(threads[i].joinable()){
            threads[i].join();
        }
    }
    auto end = chrono::steady_clock::now();
    cout << "Slept for " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;
    return 0;*/
    // Load model
    std::unique_ptr<tflite::FlatBufferModel> model =
        tflite::FlatBufferModel::BuildFromFile(filename);
    TFLITE_MINIMAL_CHECK(model != nullptr);

    // Build the interpreter
    tflite::ops::builtin::BuiltinOpResolver resolver;
    InterpreterBuilder builder(*model, resolver);
    std::unique_ptr<Interpreter> interpreter;
    builder(&interpreter);
    TFLITE_MINIMAL_CHECK(interpreter != nullptr);

    // Allocate tensor buffers.
    TFLITE_MINIMAL_CHECK(interpreter->AllocateTensors() == kTfLiteOk);

    vector<int> inputs = interpreter->inputs();
    vector<int> outputs = interpreter->outputs();
    cout << "Input indexes: " << endl;
    for(int i=0;i<inputs.size();i++){
        cout << inputs[i] << " ";
    }
    cout << endl;
    cout << "Output indexes: " << endl;
    for(int i=0;i<outputs.size();i++){
        cout << outputs[i] << " ";
    }
    cout << endl;
    // Assuming we have only one input, which is at index 0
    int input_index = interpreter->inputs()[0];
    TfLiteIntArray* dims = interpreter->tensor(input_index)->dims;
    int image_height = dims->data[1];
    int image_width = dims->data[2];
    int image_channel = dims->data[3];
    cout << "Input tensor shape: " << image_height << " " << image_width << " " << image_channel << endl;
    int number_of_pixels = image_height * image_width * image_channel;

    // Now, we will initialize the imputs val number of times and invoke the inference val number of times.
    // For each run, we will note the runtime (input buffer allocation + model runtime)
    //vector<int> runtimes;
    int diff;
    vector<int> thread_tries = {1, 2, 4, 8, 16};
    vector<int> nr_load_checkpoints = {300, 200, 100, 50, 20, 10, 5, 3,2,1};
    for(int i=0;i<thread_tries.size();i++){
        for(int j = 0;j<nr_load_checkpoints.size();j++){
            cout << "Number of threads: " << thread_tries[i] << endl;
            cout << "Workload time in millisecond: " << compute_time << endl;
            cout << "Sleep time in millisecond: " << nr_load_checkpoints[j] << endl;
            vector<thread> threads;
            for(int k=0;k<thread_tries[i];k++){
                thread th(workload, val*thread_time, compute_time, nr_load_checkpoints[j]);
                threads.push_back(std::move(th));
            }
            cout << "Thread started, starting inference" << endl;
            for(int k=0;k<val;k++){
                start = chrono::steady_clock::now();
                // setup the buffer
                auto input = interpreter->typed_tensor<float>(0);
                for(int i = 0; i < number_of_pixels; i++) {
                    input[i] = 1;
                }
                //end = chrono::steady_clock::now();
                //diff = chrono::duration_cast<chrono::milliseconds>(end - start).count();
                //cout << " Run " << i+1 << " (input buffer initialization): " << diff << endl;
                // input buffer filled, now invoke inferences
                TFLITE_MINIMAL_CHECK(interpreter->Invoke() == kTfLiteOk);
                end = chrono::steady_clock::now();
                diff = chrono::duration_cast<chrono::milliseconds>(end - start).count();
                cout << " Run " << k+1 << ": " << diff << "ms" << endl;
                //runtimes.push_back(diff);
            }
            cout << "Joining the threads" << endl;
            for(int k=0;k<thread_tries[i];k++){
                if(threads[k].joinable()){
                    threads[k].join();
                }
            }
            cout << "Thread joined" << endl;
            cout << endl;
        }
    }
    cout  << "Ending program" << endl;
    return 0;
}
