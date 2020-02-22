# TFLite model converter from saved models

import tensorflow as tf


def main():
    saved_model_dir = "."
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    tflite_model = converter.convert()
    open("model.tflite", "wb").write(tflite_model)

    print("Model is converted")

if __name__ == "__main__":
    main()
