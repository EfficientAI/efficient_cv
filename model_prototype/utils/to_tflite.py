
import os
import sys
from utils import stringify
import torch
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf

sys.path.append(os.path.abspath('.'))

from model.branchyNet import model as model_def
from dataset.cifar10 import dataset

is_cuda = torch.cuda.is_available()
device = torch.device("cuda" if is_cuda else "cpu")

"""
pytorch installation: torch==1.3.1+cpu torchvision==0.4.2+cpu
onnx: onnx==1.5
tensorflow: tensorflow==1.15.0
"""


def main():
    config = {'learning_rate': 0.001,
              'nr_epochs': 200,
              'batch_size': 8}
    data_path = 'temp/dataset'
    model_path = 'temp/saved_models'
    model_name = stringify(["model_"] +
                           [str(k)+'_'+str(config[k]) for k in config
                           if type(config[k]) == int or
                           type(config[k]) == float])+'.pt'
    model_file = os.path.join(model_path, model_name)
    model_inference = model_def()
    model_inference.load_state_dict(torch.load(model_file,
                                               map_location=device))
    # model_inference.eval()
    test_dataset = dataset(data_path, split='test')
    img, _ = test_dataset[0]
    img.unsqueeze_(0)
    img = img.data.numpy()
    dummy_input = torch.from_numpy(img).float().to(device)
    dummy_out1, dummy_out2, dummy_out3, dummy_out4 = model_inference(
                                                                   dummy_input)
    print(dummy_out1.size())
    print(dummy_out2.size())
    print(dummy_out3.size())
    print(dummy_out4.size())

    torch.onnx.export(model_inference, dummy_input,
                      os.path.join(model_path, 'model.onnx'),
                      input_names=['input'],
                      output_names=['out1', 'out2', 'out3', 'out4'])
    model_onnx = onnx.load(os.path.join(model_path, 'model.onnx'))
    tf_rep = prepare(model_onnx)
    tf_rep.export_graph(os.path.join(model_path, 'model.pb'))
    graph_def_file = os.path.join(model_path, 'model.pb')
    input_arrays = ["input"]
    output_arrays = ["out1", "out2", "out3", "out4"]
    converter = tf.lite.TFLiteConverter.from_frozen_graph(
        graph_def_file, input_arrays, output_arrays)
    tflite_model = converter.convert()
    open(os.path.join(model_path, "model.tflite"), "wb").write(tflite_model)

    # Generate sub-models
    for i in range(1, 5):
        output_arrays = ['out'+str(i)]
        converter = tf.lite.TFLiteConverter.from_frozen_graph(
            graph_def_file, input_arrays, output_arrays)
        tflite_model = converter.convert()
        model_name = "model_{}.tflite".format(i)
        open(os.path.join(model_path, model_name), "wb").write(tflite_model)


if __name__ == "__main__":
    main()
