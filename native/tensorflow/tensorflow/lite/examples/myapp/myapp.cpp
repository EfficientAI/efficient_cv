#include <cstdio>
#include <cstdlib>
#include <sstream>
#include <iostream>
#include <vector>
#include <chrono>
#include <unistd.h>

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

int main(int argc, char* argv[]) {
    //cout << "myapp program" << endl;
    auto start = chrono::steady_clock::now();
    sleep(1);
    auto end = chrono::steady_clock::now();
    //cout << "Slept for " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;
    if (argc != 3) {
        fprintf(stderr, "myapp <tflite model> nr_runs\n");
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
    //cout << "Input indexes: " << endl;
    for(int i=0;i<inputs.size();i++){
        cout << inputs[i] << " ";
    }
    //cout << endl;
    //cout << "Output indexes: " << endl;
    for(int i=0;i<outputs.size();i++){
        //cout << outputs[i] << " ";
    }
    //cout << endl;
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
    int diff;
    for(int i=0;i<val;i++){
          start = chrono::steady_clock::now();
          // setup the buffer
          auto input = interpreter->typed_tensor<float>(0);
          for(int i = 0; i < number_of_pixels; i++) {
            input[i] = 1;
          }
          end = chrono::steady_clock::now();
          diff = chrono::duration_cast<chrono::milliseconds>(end - start).count();
          // cout << " Run " << i+1 << " (input buffer initialization): " << diff << endl;
          // input buffer filled, now invoke inferences
          TFLITE_MINIMAL_CHECK(interpreter->Invoke() == kTfLiteOk);
          end = chrono::steady_clock::now();
          diff = chrono::duration_cast<chrono::milliseconds>(end - start).count();
          //cout << " Run " << i+1 << " (total): " << diff << endl;
          runtimes.push_back(diff);
    }
    cout << "Runtimes were: ";
    for(int i=0;i<runtimes.size();i++){
        cout << runtimes[i] << " ";
    }
    cout << endl;
    cout  << "Ending program" << endl;
    return 0;
}
