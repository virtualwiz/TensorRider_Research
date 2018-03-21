import numpy as np
from skimage import io
from matplotlib import pyplot as plt
import tensorflow as tf

record_iterator = tf.python_io.tf_record_iterator(path="record.tfrecords")

for string_record in record_iterator:
    example = tf.train.Example()
    example.ParseFromString(string_record)

    imageString = (example.features.feature['image_string'].bytes_list.value[0])

    label = (example.features.feature['label'].int64_list.value[0])

    image_1d = np.fromstring(imageString, dtype=np.uint8)
    image = image_1d.reshape((120, 160, 1))

    io.imshow(image)
    plt.show()

    read();
