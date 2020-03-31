#include <cstdio>
#include <cstdlib>
#include <fstream>
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

// Usage: myapp <tflite model> nr_runs
using namespace std;
using namespace tflite;

#define TFLITE_MINIMAL_CHECK(x)                              \
  if (!(x)) {                                                \
    fprintf(stderr, "Error at %s:%d\n", __FILE__, __LINE__); \
    exit(1);                                                 \
  }

const int NUM_CPU_STATES = 10;

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

typedef struct CPUData
{
	std::string cpu;
	size_t times[NUM_CPU_STATES];
} CPUData;

void ReadStatsCPU(std::vector<CPUData> & entries)
{
	std::ifstream fileStat("/proc/stat");

	std::string line;

	const std::string STR_CPU("cpu");
	const std::size_t LEN_STR_CPU = STR_CPU.size();
	const std::string STR_TOT("tot");

	while(std::getline(fileStat, line))
	{
		// cpu stats line found
		if(!line.compare(0, LEN_STR_CPU, STR_CPU))
		{
			std::istringstream ss(line);

			// store entry
			entries.emplace_back(CPUData());
			CPUData & entry = entries.back();

			// read cpu label
			ss >> entry.cpu;

			// remove "cpu" from the label when it's a processor number
			if(entry.cpu.size() > LEN_STR_CPU)
				entry.cpu.erase(0, LEN_STR_CPU);
			// replace "cpu" with "tot" when it's total values
			else
				entry.cpu = STR_TOT;

			// read times
			for(int i = 0; i < NUM_CPU_STATES; ++i)
				ss >> entry.times[i];
		}
	}
}

size_t GetIdleTime(const CPUData & e)
{
	return	e.times[S_IDLE] + 
			e.times[S_IOWAIT];
}

size_t GetActiveTime(const CPUData & e)
{
	return	e.times[S_USER] +
			e.times[S_NICE] +
			e.times[S_SYSTEM] +
			e.times[S_IRQ] +
			e.times[S_SOFTIRQ] +
			e.times[S_STEAL] +
			e.times[S_GUEST] +
			e.times[S_GUEST_NICE];
}

float get_avg_load(int sleep_time){
	std::vector<CPUData> entries1;
	std::vector<CPUData> entries2;
	ReadStatsCPU(entries1);
	std::this_thread::sleep_for(std::chrono::milliseconds(sleep_time));
	ReadStatsCPU(entries2);
	const size_t NUM_ENTRIES = entries1.size();
	float avg_load = 0.0;
	const CPUData & e1 = entries1[0];
	const CPUData & e2 = entries2[0];
	const float ACTIVE_TIME	= static_cast<float>(GetActiveTime(e2) - GetActiveTime(e1));
	const float IDLE_TIME	= static_cast<float>(GetIdleTime(e2) - GetIdleTime(e1));
	const float TOTAL_TIME	= ACTIVE_TIME + IDLE_TIME;
	avg_load = (100.f * ACTIVE_TIME / TOTAL_TIME);
	return avg_load;
}

float get_avg_load_avg(int sleep_time, int nr_instances){
    float total_avg_load = 0.0;
    for(int j=0;j<nr_instances;j++){
        total_avg_load += get_avg_load(sleep_time);
    }
    total_avg_load = total_avg_load/float(nr_instances);
    return total_avg_load;
}

int main(int argc, char* argv[]) {
    //cout << "myapp program" << endl;
    auto start = chrono::steady_clock::now();
    sleep(1);
    auto end = chrono::steady_clock::now();
    //cout << "Slept for " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;
    if (argc != 3) {
        fprintf(stderr, "load_track_myapp <tflite model> nr_runs\n");
        return 1;
    }
    const char* filename = argv[1];
    istringstream iss(argv[2]);
    int val;
    iss >> val;
    cout << "file received: " << filename << " nr_runs received: " << val << endl;

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
    /*cout << "Input indexes: " << endl;
    for(int i=0;i<inputs.size();i++){
        cout << inputs[i] << " ";
    }
    cout << endl;
    cout << "Output indexes: " << endl;
    for(int i=0;i<outputs.size();i++){
        cout << outputs[i] << " ";
    }
    cout << endl;*/
    // Assuming we have only one input, which is at index 0
    int input_index = interpreter->inputs()[0];
    TfLiteIntArray* dims = interpreter->tensor(input_index)->dims;
    int image_height = dims->data[1];
    int image_width = dims->data[2];
    int image_channel = dims->data[3];
    //cout << "Input tensor shape: " << image_height << " " << image_width << " " << image_channel << endl;
    int number_of_pixels = image_height * image_width * image_channel;

    // Now, we will initialize the imputs val number of times and invoke the inference val number of times.
    // For each run, we will note the runtime (input buffer allocation + model runtime)
    vector<int> runtimes;
    vector<int> cpu_loads;
    int diff;
    int pause_time = 10; //in ms
    int nr_instances = 10; //records average
    for(int i=0;i<val;i++){
        cpu_loads.push_back(get_avg_load_avg(pause_time, nr_instances));
        // setup the buffer
        auto input = interpreter->typed_tensor<float>(0);
        for(int i = 0; i < number_of_pixels; i++) {
            input[i] = 1;
        }
        start = chrono::steady_clock::now();
        // cout << " Run " << i+1 << " (input buffer initialization): " << diff << endl;
        // input buffer filled, now invoke inferences
        TFLITE_MINIMAL_CHECK(interpreter->Invoke() == kTfLiteOk);
        end = chrono::steady_clock::now();
        diff = chrono::duration_cast<chrono::milliseconds>(end - start).count();
        //cout << " Run " << i+1 << " (total): " << diff << endl;
        runtimes.push_back(diff);
    }
    //cout << "Runtimes were: ";
    for(int i=0;i<runtimes.size();i++){
        cout << cpu_loads[i] << " " << runtimes[i] << " ";
    }
    cout << endl;
    cout  << "Ending program" << endl;
    return 0;
}
