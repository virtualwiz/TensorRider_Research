import numpy as np
from skimage import io
from matplotlib import pyplot as plt
import tensorflow as tf
import tensorlayer as tl

sess = tf.InteractiveSession()

def rgb2mono(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    # mono = 0.2989 * r + 0.5870 * g + 0.1140 * b
    mono = 0.5 * r + 0.25 * g + 0.25 * b
    return mono

def prepareDataArrays(iterator):
    X = np.zeros(19200)
    y = np.zeros(1)
    recordCounter = 0;

    for string_record in iterator:
        recordCounter += 1

        example = tf.train.Example()
        example.ParseFromString(string_record)
        imageString = (example.features.feature['image'].bytes_list.value[0])
        label = (example.features.feature['label'].int64_list.value[0])

        image = np.fromstring(imageString, dtype=np.uint8)
        image = image.reshape((120, 160, 3))
        image = rgb2mono(image)
        image = image.reshape((19200))

        X = np.vstack((X,image))
        y = np.append(y,label)
        if recordCounter % 100 == 0:
            print(recordCounter)

    y = y.reshape((recordCounter + 1,))
    y = np.floor(y / 6) #Downsampling
    return X, y


trainIterator = tf.python_io.tf_record_iterator(path="test.tfrecords")
valIterator = tf.python_io.tf_record_iterator(path="val.tfrecords")
testIterator = tf.python_io.tf_record_iterator(path="test.tfrecords")

print("Train...")
X_train, y_train = prepareDataArrays(trainIterator)
print("Val...")
X_val, y_val = prepareDataArrays(valIterator)
print("Test...")
X_test, y_test = prepareDataArrays(testIterator)


x = tf.placeholder(tf.float32, shape=[None, 19200], name='x')
y_ = tf.placeholder(tf.int64, shape=[None], name='y_')

# define the network
network = tl.layers.InputLayer(x, name='input')
network = tl.layers.DropoutLayer(network, keep=0.8, name='drop1')
network = tl.layers.DenseLayer(network, 1600, tf.nn.relu, name='relu1')
network = tl.layers.DropoutLayer(network, keep=0.5, name='drop2')
network = tl.layers.DenseLayer(network, 1600, tf.nn.relu, name='relu2')
network = tl.layers.DropoutLayer(network, keep=0.5, name='drop3')
network = tl.layers.DenseLayer(network, n_units=13, act=tf.identity, name='output')

# define cost function and metric.
y = network.outputs
cost = tl.cost.cross_entropy(y, y_, name='cost')
correct_prediction = tf.equal(tf.argmax(y, 1), y_)
acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
y_op = tf.argmax(tf.nn.softmax(y), 1)

# define the optimizer
train_params = network.all_params
train_op = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost, var_list=train_params)

# initialize all variables in the session
tl.layers.initialize_global_variables(sess)

# print network information
network.print_params()
network.print_layers()


# train the network
tl.utils.fit(
    sess, network, train_op, cost, X_train, y_train, x, y_, acc=acc, batch_size=200, n_epoch=500, print_freq=5, X_val=X_val, y_val=y_val, eval_train=False)

# evaluation
tl.utils.test(sess, network, acc, X_test, y_test, x, y_, batch_size=None, cost=cost)

# save the network to .npz file
tl.files.save_npz(network.all_params, name='model.npz')
sess.close()
