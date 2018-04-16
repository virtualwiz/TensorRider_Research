import numpy as np
from skimage import io
from matplotlib import pyplot as plt
import linecache
import tensorflow as tf

PATH_T1 = "./train_a/"
NUM_OF_IMAGES_T1 = 10000
PATH_T2 = "./train_b/"
NUM_OF_IMAGES_T2 = 10000
PATH_T3 = "./train_c/"
NUM_OF_IMAGES_T3 = 10000

PATH_V1 = "./val_a/"
NUM_OF_IMAGES_V1 = 1739
PATH_V2 = "./val_b/"
NUM_OF_IMAGES_V2 = 3261

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _float32_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def convertOneFolder(path, num):
    global tfWriter
    for fileIndex in range(1, int(num)+1):
        image = io.imread(path + "%0*d" %(6, fileIndex) + ".jpg")
        
        imageString = image.tostring()

        direction = int(linecache.getline(path + "steer_log.txt", fileIndex))

        example = tf.train.Example(features=tf.train.Features(feature={
            'image': _bytes_feature(imageString),
            'label': _int64_feature(direction)
        }))

        print("Writing record " + "%0*d" %(6, fileIndex) + ".jpg " + "with label " + str(direction))
        tfWriter.write(example.SerializeToString())



tfrecords_filename = 'train.tfrecords'
tfWriter = tf.python_io.TFRecordWriter(tfrecords_filename)

convertOneFolder(PATH_T1, NUM_OF_IMAGES_T1)
convertOneFolder(PATH_T2, NUM_OF_IMAGES_T2)
convertOneFolder(PATH_T3, NUM_OF_IMAGES_T3)

tfWriter.close()



tfrecords_filename = 'val.tfrecords'
tfWriter = tf.python_io.TFRecordWriter(tfrecords_filename)

convertOneFolder(PATH_V1, NUM_OF_IMAGES_V1)
convertOneFolder(PATH_V2, NUM_OF_IMAGES_V2)

tfWriter.close()
