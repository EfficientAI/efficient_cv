# BUILD script for final_app

load("//tensorflow/lite:build_def.bzl", "tflite_linkopts")

package(
    default_visibility = ["//visibility:public"],
    licenses = ["notice"],  # Apache 2.0
)

cc_binary(
    name = "final_app",
    srcs = [
        "final_app.cpp",
    ],
    linkopts = tflite_linkopts() + select({
        "//tensorflow:android": [
            "-pie",  # Android 5.0 and later supports only PIE
            "-lm",  # some builtin ops, e.g., tanh, need -lm
        ] + ["-pthread"],
        "//conditions:default": [],
    }),
    deps = [
        "//tensorflow/lite:framework",
        "//tensorflow/lite/kernels:builtin_ops",
    ],
)
