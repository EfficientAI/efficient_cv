# Cross-compiling tflite for Android devices

Although the official tensorflow lite [documentation](https://www.tensorflow.org/lite/guide/android) gives a starighforward steps to build tflite application, there are still a **lot** of moving parts like Bazel version, NDK version, SDK version, tensorflow configuration etc.
The motivation of this document is to provide a detailed step-to-step process to get tflite building and an executable program that can run on Andoroid Phones.

## Step 1: Downloading the dependancies
### Bazel
Download the tesorflow recommended version of bazel from [here](https://docs.bazel.build/versions/master/install-ubuntu.html). The recommended version is [0.29.1](https://github.com/bazelbuild/bazel/releases/tag/0.29.1). Follow the binary installer procedure.

Check the version of bazel using command 'bazel version'. It should print 0.29.1.
If you already have a bazel installed, remove it using 'rm -fr ~/.bazel ~/.bazelrc'.

### NDK
According to documentation, you are required to get NDK version 17c. But it didnot work for me as it had toolchain without STL support. So, download NDK version r21 from [here](https://developer.android.com/ndk/downloads). Uncompress it to a folder names android_tools. Make sure the directory is called 'android-ndk-r21' (it should be one level inside after decompression).

### SDK
The best way to get SDK is to install Android Studio. Setup android studio, it will give the SDK (thats what worked for me). Otherwise, latest SDK can be downloaded from official Android [website](https://developer.android.com/studio).

Again make sure the folder is called 'Sdk' with folders like tools, fonts, etc. inside.

### Tensorflow
Clone the latest tensorflow version, and to be on the safe side, do 'git checkout r2.1'. This will checkout a release version of tensorflow.

## Step 2: Setting up tensorflow lite for building
### SDK and NDK configuration
The best way to tell tensorflow where to look for NDK (which will give the compilation tool chain) and SDK is to execute configure. Go to the tensorflow root, and type './configure'.

The program will interactively ask a lot of questions. First several questions are useless, just say n to those, then it will ask to configure workspace. Say 'y' to it. It will ask the paths and version of NDK and SDK. Input these properly. The full commands I gave is given below:

```
WARNING: Running Bazel server needs to be killed, because the startup options are different.
WARNING: Waiting for server process to terminate (waited 5 seconds, waiting at most 60)
WARNING: --batch mode is deprecated. Please instead explicitly shut down your Bazel server using the command "bazel shutdown".
You have bazel 0.29.1 installed.
Please specify the location of python. [Default is /usr/bin/python]: 

Found possible Python library paths:
  /usr/local/lib/python2.7/dist-packages
  /usr/lib/python2.7/dist-packages
Please input the desired Python library path to use.  Default is [/usr/local/lib/python2.7/dist-packages]

Do you wish to build TensorFlow with XLA JIT support? [Y/n]: n
No XLA JIT support will be enabled for TensorFlow.

Do you wish to build TensorFlow with OpenCL SYCL support? [y/N]: N
No OpenCL SYCL support will be enabled for TensorFlow.

Do you wish to build TensorFlow with ROCm support? [y/N]: N
No ROCm support will be enabled for TensorFlow.

Do you wish to build TensorFlow with CUDA support? [y/N]: N
No CUDA support will be enabled for TensorFlow.

Do you wish to download a fresh release of clang? (Experimental) [y/N]: y
Clang will be downloaded and used to compile tensorflow.

Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -march=native -Wno-sign-compare]: 

Would you like to interactively configure ./WORKSPACE for Android builds? [y/N]: y
Searching for NDK and SDK installations.

Please specify the home path of the Android NDK to use. [Default is /home/vishal/Android/Sdk/ndk-bundle]: /home/vishal/android_tools/android-ndk-r21

WARNING: The NDK version in /home/vishal/android_tools/android-ndk-r21 is 21, which is not supported by Bazel (officially supported versions: [10, 11, 12, 13, 14, 15, 16, 17, 18]). Please use another version. Compiling Android targets may result in confusing errors.

Please specify the (min) Android NDK API level to use. [Available levels: ['16', '17', '18', '19', '21', '22', '23', '24', '26', '27', '28', '29']] [Default is 21]: 28

Please specify the home path of the Android SDK to use. [Default is /home/vishal/Android/Sdk]: 

Please specify the Android SDK API level to use. [Available levels: ['29']] [Default is 29]: 29

Please specify an Android build tools version to use. [Available versions: ['29.0.2']] [Default is 29.0.2]: 29.0.2

Preconfigured Bazel build configs. You can use any of the below by adding "--config=<>" to your build command. See .bazelrc for more details.
	--config=mkl         	# Build with MKL support.
	--config=monolithic  	# Config for mostly static monolithic build.
	--config=ngraph      	# Build with Intel nGraph support.
	--config=numa        	# Build with NUMA support.
	--config=dynamic_kernels	# (Experimental) Build kernels into separate shared objects.
	--config=v2          	# Build TensorFlow 2.x instead of 1.x.
Preconfigured Bazel build configs to DISABLE default on features:
	--config=noaws       	# Disable AWS S3 filesystem support.
	--config=nogcp       	# Disable GCP support.
	--config=nohdfs      	# Disable HDFS support.
	--config=nonccl      	# Disable NVIDIA NCCL support.
Configuration finished
```

Note that I have chosen NDK API level 28 and SDK API level 29.

## Step 3: Creating an application and building it with tflite framework as a dependancy
For this part, we can either just build the minimal.cc code or write our own cpp files.
I always write a test program to make sure my changes will be reflected when I develop a bigger program.

### Write a test program
Create a file called test.cpp in the directory tensorflow/lite/examples/minimal/test.cpp.

Paste the below code in that file:

```C++
#include <cstdio>
#include <iostream>
#include <vector>
#include <chrono>
#include <unistd.h>

#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/optional_debug_tools.h"

// Usage: minimal <tflite model>
using namespace std;
using namespace tflite;

#define TFLITE_MINIMAL_CHECK(x)                              \
  if (!(x)) {                                                \
    fprintf(stderr, "Error at %s:%d\n", __FILE__, __LINE__); \
    exit(1);                                                 \
  }

int main(int argc, char* argv[]) {
    cout << "Testing a sample program running on Android" << endl;
    auto start = chrono::steady_clock::now();
    sleep(3);
    auto end = chrono::steady_clock::now();
    cout << "Slept for " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << endl;
    if (argc != 2) {
        fprintf(stderr, "minimal <tflite model>\n");
        return 1;
    }
    const char* filename = argv[1];

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
    printf("=== Pre-invoke Interpreter State ===\n");
    tflite::PrintInterpreterState(interpreter.get());

    // Fill input buffers
    // TODO(user): Insert code to fill input tensors

    // Run inference
    TFLITE_MINIMAL_CHECK(interpreter->Invoke() == kTfLiteOk);
    printf("\n\n=== Post-invoke Interpreter State ===\n");
    tflite::PrintInterpreterState(interpreter.get());

    // Read output buffers
    // TODO(user): Insert getting data out code.

    return 0;
}
```
### Configure bazel compilation to build your program

Since the test.cpp uses several headers from tflite, all these dependancies are being packed in 'framework' module in the tflite BUILD.
We just need to point out to 'framework' as a dependancy to build out test.cpp.

Append the below code in tensorflow/lite/examples.minimal/BUILD
```
cc_binary(
    name = "test",
    srcs = [
        "test.cpp",
    ],
    linkopts = tflite_linkopts() + select({
        "//tensorflow:android": [
            "-pie",  # Android 5.0 and later supports only PIE
            "-lm",  # some builtin ops, e.g., tanh, need -lm
        ],
        "//conditions:default": [],
    }),
    deps = [
        "//tensorflow/lite:framework",
        "//tensorflow/lite/kernels:builtin_ops",
    ],
)
```

## Step 4: Building with correct bazel command.
It is very essential to correctly set the flags before building your program using bazel build.

In terminal, go to the tensorflow root director, and type this:

```
bazel build  --config android_arm64 //tensorflow/lite/examples/minimal:test --config monolithic
```

The bazel maximizes the number of threads to compilation process, which will eventually hang your system, so you might want to restrict the number of compilation threads using the below build command instead:

```
bazel build --jobs 4 --config android_arm64 //tensorflow/lite/examples/minimal:test --config monolithic
```

## Step 5: Testing the program.
Copy the executable in bazel-bin/tensorflow/lite/examples/minimal/test to /data/local/tmp folder in Android.

```
adb push bazel-bin/tensorflow/lite/examples/minimal/test /data/local/tmp
```

Then in adb shell, go to /data/local/tmp and execute the test

```
./test
```

# Futher
I will keep on updating this document as I see any further issues.