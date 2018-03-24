import os
import numpy as np
import tensorflow as tf
import tensorlayer as tl

def read_and_decode(filename):
    # generate a queue with a given file name
    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)  # return the file and the name of file
    features = tf.parse_single_example(
        serialized_example,  # see parse_single_sequence_example for sequence example
        features={
            'label': tf.FixedLenFeature([], tf.int64),
            'image': tf.FixedLenFeature([], tf.string),
        })
    # You can do more image distortion here for training data
    img = tf.decode_raw(features['image'], tf.uint8)
    img = tf.reshape(img, [120, 160, 3])
    gimg = tf.image.rgb_to_grayscale(img)
    label = tf.cast(features['label'], tf.int64)
    return img, gimg, label

img, gimg, label = read_and_decode("train.tfrecords")


print(img)
print(gimg)
print(label)


img_batch, label_batch = tf.train.shuffle_batch([img, label], batch_size=16, capacity=30, min_after_dequeue=10, num_threads=8)

print(img_batch)
print(label_batch)




# with tf.Session() as sess:
#     tl.layers.initialize_global_variables(sess)
#     coord = tf.train.Coordinator()
#     threads = tf.train.start_queue_runners(sess=sess, coord=coord)

#     for i in range(500):  # number of mini-batch (step)
#         print("Step %d" % i)
#         val, l = sess.run([img_batch, label_batch])
#         print(val.shape, l)
#         tl.visualize.images2d(val, second=1, saveable=False, name='batch', dtype=None, fig_idx=2020121)

#     coord.request_stop()
#     coord.join(threads)
#     sess.close()