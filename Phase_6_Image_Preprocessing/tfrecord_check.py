import numpy as np
from skimage import io
from matplotlib import pyplot as plt
import tensorflow as tf

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    gray = 0.5 * r + 0.25 * g + 0.25 * b
    return gray

record_iterator = tf.python_io.tf_record_iterator(path="record.tfrecords")

for string_record in record_iterator:
    example = tf.train.Example()
    example.ParseFromString(string_record)

    imageString = (example.features.feature['image'].bytes_list.value[0])

    label = (example.features.feature['label'].int64_list.value[0])

    image_1d = np.fromstring(imageString, dtype=np.uint8)
    image = image_1d.reshape((120, 160, 3))
    image = rgb2gray(image)

    print(image.shape)

    io.imshow(image)
    plt.show()

