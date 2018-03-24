import numpy as np
from skimage import io
from matplotlib import pyplot as plt
import tensorflow as tf

def rgb2mono(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    # mono = 0.2989 * r + 0.5870 * g + 0.1140 * b
    mono = 0.5 * r + 0.25 * g + 0.25 * b
    return mono

trainIterator = tf.python_io.tf_record_iterator(path="train.tfrecords")
valIterator = tf.python_io.tf_record_iterator(path="val.tfrecords")
testIterator = tf.python_io.tf_record_iterator(path="test.tfrecords")

# X_train, y_train, X_val, y_val, X_test, y_test = \
#                 tl.files.load_mnist_dataset(shape=(-1, 28, 28, 1))

def prepareDataArrays(iterator):
    for string_record in iterator:
        example = tf.train.Example()
        example.ParseFromString(string_record)
        imageString = (example.features.feature['image'].bytes_list.value[0])
        label = (example.features.feature['label'].int64_list.value[0])

        image = np.fromstring(imageString, dtype=np.uint8)
        image = image.reshape((120, 160, 3))
        image = rgb2mono(image)
        image = image.reshape((19200))
