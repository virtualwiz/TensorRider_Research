import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf
import skimage.io as io

tfrecords_filename = 'record.tfrecords'

def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()

    _, serialized_example = reader.read(filename_queue)

    features = tf.parse_single_example(
        serialized_example,
        features={
        'image': tf.FixedLenFeature([], tf.string),
        'label': tf.FixedLenFeature([], tf.int64)
        })

    image = tf.decode_raw(features['image'], tf.uint8)
    label = tf.cast(features['label'], tf.int64)

    height = tf.cast(120, tf.int32)
    width = tf.cast(160, tf.int32)

    image = tf.reshape(image, [height, width, 3])
    imageGrayScaled = tf.image.rgb_to_grayscale(image)

    images, labels = tf.train.shuffle_batch(
        [imageGrayScaled, label],
        batch_size=2,
        capacity=30,
        num_threads=1,
        min_after_dequeue=10)

    return images, labels

filename_queue = tf.train.string_input_producer(
     [tfrecords_filename], num_epochs=10)

images, labels = read_and_decode(filename_queue)

init_op = tf.group(tf.global_variables_initializer(),
                   tf.local_variables_initializer())

with tf.Session()  as sess:
    sess.run(init_op)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(5):    

        img, lab = sess.run([images, labels])

        # 檢查每個 batch 的圖片維度
        print(img.shape)

        # 顯示每個 batch 的第一張圖
        io.imshow(img[0, :, :, 0])
        plt.show()

    coord.request_stop()
    coord.join(threads)