# Converting frozen pb files to tflite file
# See guide "Converting_to_tflite_guide.md" for more details

import tensorflow as tf

graph_def_file = "model.pb"
input_arrays = ["model_inputs"]
output_arrays = ["model_outputs"]

converter = tf.lite.TFLiteConverter.from_frozen_graph(
        graph_def_file, input_arrays, output_arrays)
tflite_model = converter.convert()
open("converted_model.tflite", "wb").write(tflite_model)