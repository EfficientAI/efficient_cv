import os
import sys
import numpy as np
import tensorflow as tf

sys.path.append(os.path.abspath('.'))
from dataset.cifar10 import dataset
from torch.utils.data import DataLoader


def calculate_accuracy(interpreter, val_loader):
    corrects = [0.0]*4
    total = 0
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    for batch_idx, data in enumerate(val_loader, start=0):
        img, label = data
        img = img.data.numpy()
        label = label.data.numpy()[0]
        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()
        o1, o2, o3, o4 = interpreter.get_tensor(output_details[0]['index']),\
            interpreter.get_tensor(output_details[1]['index']),\
            interpreter.get_tensor(output_details[2]['index']),\
            interpreter.get_tensor(output_details[3]['index'])
        outputs = [o1, o2, o3, o4]
        for i, output in enumerate(outputs):
            predicted = np.argmax(output[0])
            corrects[i] += np.sum((predicted == label))
        total += 1.0
    corrects = np.array(corrects)
    return (corrects*100)/float(total)


def main():
    data_path = 'temp/dataset'
    model_path = 'temp/saved_models'
    model_name = 'model.tflite'
    interpreter = tf.lite.Interpreter(model_path=os.path.join(
        model_path, model_name))
    interpreter.allocate_tensors()
    test_dataset = dataset(data_path, split='test')
    test_loader = DataLoader(test_dataset, batch_size=1,
                             shuffle=False)
    accuracies = calculate_accuracy(interpreter, test_loader)
    print(accuracies)


if __name__ == "__main__":
    main()
