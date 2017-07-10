import time,sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append('../')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity as af123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#from af_utils import geom_utils123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#from af_nn import nn_ops123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#from af_input import av4_input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# telling tensorflow how we want to randomly initialize weights123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef weight_variable(shape):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial = tf.truncated_normal(shape, stddev=0.005)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.Variable(initial)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef bias_variable(shape):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial = tf.constant(0.01, shape=shape)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.Variable(initial)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef variable_summaries(var, name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """attaches a lot of summaries to a tensor."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('summaries'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        mean = tf.reduce_mean(var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('mean/' + name, mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('stddev'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('stddev/' + name, stddev)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('max/' + name, tf.reduce_max(var))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('min/' + name, tf.reduce_min(var))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.histogram(name, var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef conv_layer(layer_name, input_tensor, filter_size, strides=[1, 1, 1, 1, 1], padding='SAME'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """makes a simple convolutional layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    input_depth = filter_size[3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    output_depth = filter_size[4]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        with tf.name_scope('weights'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            W_conv = weight_variable(filter_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            variable_summaries(W_conv, layer_name + '/weights')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        with tf.name_scope('biases'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            b_conv = bias_variable([output_depth])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            variable_summaries(b_conv, layer_name + '/biases')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            h_conv = tf.nn.conv3d(input_tensor, W_conv, strides=strides, padding=padding) + b_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tf.summary.histogram(layer_name + '/pooling_output', h_conv)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print layer_name,"output dimensions:", h_conv.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return h_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef relu_layer(layer_name,input_tensor,act=tf.nn.relu):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """makes a simple relu layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_relu = act(input_tensor, name='activation')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.histogram(layer_name + '/relu_output', h_relu)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar(layer_name + '/sparsity', tf.nn.zero_fraction(h_relu))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print layer_name, "output dimensions:", h_relu.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return h_relu123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef pool_layer(layer_name,input_tensor,ksize,strides=[1, 1, 1, 1, 1],padding='SAME'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """makes a simple max pooling layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool = tf.nn.max_pool3d(input_tensor,ksize=ksize,strides=strides,padding=padding)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.histogram(layer_name + '/max_pooling_output', h_pool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print layer_name, "output dimensions:", h_pool.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return h_pool123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef avg_pool_layer(layer_name,input_tensor,ksize,strides=[1, 1, 1, 1, 1],padding='SAME'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """makes a average pooling layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool = tf.nn.avg_pool3d(input_tensor,ksize=ksize,strides=strides,padding=padding)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.histogram(layer_name + '/average_pooling_output', h_pool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print layer_name, "output dimensions:", h_pool.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return h_pool123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef fc_layer(layer_name,input_tensor,output_dim):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """makes a simple fully connected layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    input_dim = int((input_tensor.get_shape())[1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        weights = weight_variable([input_dim, output_dim])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        variable_summaries(weights, layer_name + '/weights')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('biases'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        biases = bias_variable([output_dim])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        variable_summaries(biases, layer_name + '/biases')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('Wx_plus_b'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc = tf.matmul(input_tensor, weights) + biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.histogram(layer_name + '/fc_output', h_fc)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print layer_name, "output dimensions:", h_fc.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return h_fc123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef old_max_net(x_image_batch,keep_prob,batch_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "makes a simple network that can receive 20x20x20 input images. And output 2 classes"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('input'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("input_reshape"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "image batch dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # formally adding one depth dimension to the input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        x_image_batch = tf.reshape(x_image_batch, [batch_size, 20, 20, 20, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "input to the first layer dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv1 = conv_layer(layer_name='conv1_5x5x5', input_tensor=x_image_batch, filter_size=[5, 5, 5, 1, 20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu1 = relu_layer(layer_name='relu1', input_tensor=h_conv1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool1 = pool_layer(layer_name='pool1_2x2x2', input_tensor=h_relu1, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv2 = conv_layer(layer_name="conv2_3x3x3", input_tensor=h_pool1, filter_size=[3, 3, 3, 20, 30])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu2 = relu_layer(layer_name="relu2", input_tensor=h_conv2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool2 = pool_layer(layer_name="pool2_2x2x2", input_tensor=h_relu2, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv3 = conv_layer(layer_name="conv3_2x2x2", input_tensor=h_pool2, filter_size=[2, 2, 2, 30, 40])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu3 = relu_layer(layer_name="relu3", input_tensor=h_conv3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool3 = pool_layer(layer_name="pool3_2x2x2", input_tensor=h_relu3, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv4 = conv_layer(layer_name="conv4_2x2x2", input_tensor=h_pool3, filter_size=[2, 2, 2, 40, 50])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu4 = relu_layer(layer_name="relu4", input_tensor=h_conv4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool4 = pool_layer(layer_name="pool4_2x2x2", input_tensor=h_relu4, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv5 = conv_layer(layer_name="conv5_2x2x2", input_tensor=h_pool4, filter_size=[2, 2, 2, 50, 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu5 = relu_layer(layer_name="relu5", input_tensor=h_conv5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool5 = pool_layer(layer_name="pool5_2x2x2", input_tensor=h_relu5, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("flatten_layer"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool2_flat = tf.reshape(h_pool5, [-1, 5 * 5 * 5 * 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1 = fc_layer(layer_name="fc1", input_tensor=h_pool2_flat, output_dim=1024)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1_relu = relu_layer(layer_name="fc1_relu", input_tensor=h_fc1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("dropout"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('dropout_keep_probability', keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1_drop = tf.nn.dropout(h_fc1_relu, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2 = fc_layer(layer_name="fc2", input_tensor=h_fc1_drop, output_dim=256)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2_relu = relu_layer(layer_name="fc2_relu", input_tensor=h_fc2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = fc_layer(layer_name="out_neuron", input_tensor=h_fc2_relu, output_dim=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return y_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef ag_net(x_image_batch,keep_prob,batch_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "makes a simple network that can receive 20x20x20 input images. And output 2 classes"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('input'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("input_reshape"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "image batch dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # formally adding one depth dimension to the input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        x_image_batch = tf.reshape(x_image_batch, [batch_size, 20, 20, 20, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "input to the first layer dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv1 = conv_layer(layer_name='conv1_5x5x5', input_tensor=x_image_batch, filter_size=[5, 5, 5, 1, 20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu1 = relu_layer(layer_name='relu1', input_tensor=h_conv1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool1 = pool_layer(layer_name='pool1_2x2x2', input_tensor=h_relu1, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv2 = conv_layer(layer_name="conv2_3x3x3", input_tensor=h_pool1, filter_size=[3, 3, 3, 20, 30])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu2 = relu_layer(layer_name="relu2", input_tensor=h_conv2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool2 = pool_layer(layer_name="pool2_2x2x2", input_tensor=h_relu2, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv3 = conv_layer(layer_name="conv3_2x2x2", input_tensor=h_pool2, filter_size=[2, 2, 2, 30, 40])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu3 = relu_layer(layer_name="relu3", input_tensor=h_conv3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool3 = pool_layer(layer_name="pool3_2x2x2", input_tensor=h_relu3, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv4 = conv_layer(layer_name="conv4_2x2x2", input_tensor=h_pool3, filter_size=[2, 2, 2, 40, 50])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu4 = relu_layer(layer_name="relu4", input_tensor=h_conv4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool4 = pool_layer(layer_name="pool4_2x2x2", input_tensor=h_relu4, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv5 = conv_layer(layer_name="conv5_2x2x2", input_tensor=h_pool4, filter_size=[2, 2, 2, 50, 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu5 = relu_layer(layer_name="relu5", input_tensor=h_conv5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool5 = pool_layer(layer_name="pool5_2x2x2", input_tensor=h_relu5, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("flatten_layer"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool2_flat = tf.reshape(h_pool5, [-1, 5 * 5 * 5 * 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1 = fc_layer(layer_name="fc1", input_tensor=h_pool2_flat, output_dim=1024)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1_relu = relu_layer(layer_name="fc1_relu", input_tensor=h_fc1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("dropout"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('dropout_keep_probability', keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1_drop = tf.nn.dropout(h_fc1_relu, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2 = fc_layer(layer_name="fc2", input_tensor=h_fc1_drop, output_dim=256)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2_relu = relu_layer(layer_name="fc2_relu", input_tensor=h_fc2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = fc_layer(layer_name="out_neuron", input_tensor=h_fc2_relu, output_dim=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return y_conv#tf.reshape(y_conv,[batch_size,1,3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef ag_net_2(x_image_batch,keep_prob,batch_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "makes a simple network that can receive 20x20x20 input images. And output 2 classes"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('input'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("input_reshape"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "image batch dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # formally adding one depth dimension to the input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #x_image_batch = tf.reshape(x_image_batch, [batch_size, 20, 20, 20, 2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "input to the first layer dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv1 = conv_layer(layer_name='conv1_5x5x5', input_tensor=x_image_batch, filter_size=[5, 5, 5, 2, 20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu1 = relu_layer(layer_name='relu1', input_tensor=h_conv1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool1 = pool_layer(layer_name='pool1_2x2x2', input_tensor=h_relu1, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv2 = conv_layer(layer_name="conv2_3x3x3", input_tensor=h_pool1, filter_size=[3, 3, 3, 20, 30])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu2 = relu_layer(layer_name="relu2", input_tensor=h_conv2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool2 = pool_layer(layer_name="pool2_2x2x2", input_tensor=h_relu2, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv3 = conv_layer(layer_name="conv3_2x2x2", input_tensor=h_pool2, filter_size=[2, 2, 2, 30, 40])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu3 = relu_layer(layer_name="relu3", input_tensor=h_conv3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool3 = pool_layer(layer_name="pool3_2x2x2", input_tensor=h_relu3, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv4 = conv_layer(layer_name="conv4_2x2x2", input_tensor=h_pool3, filter_size=[2, 2, 2, 40, 50])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu4 = relu_layer(layer_name="relu4", input_tensor=h_conv4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool4 = pool_layer(layer_name="pool4_2x2x2", input_tensor=h_relu4, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv5 = conv_layer(layer_name="conv5_2x2x2", input_tensor=h_pool4, filter_size=[2, 2, 2, 50, 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu5 = relu_layer(layer_name="relu5", input_tensor=h_conv5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool5 = pool_layer(layer_name="pool5_2x2x2", input_tensor=h_relu5, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("flatten_layer"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool2_flat = tf.reshape(h_pool5, [-1, 5 * 5 * 5 * 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1 = fc_layer(layer_name="fc1", input_tensor=h_pool2_flat, output_dim=1024)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1_relu = relu_layer(layer_name="fc1_relu", input_tensor=h_fc1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("dropout"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('dropout_keep_probability', keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1_drop = tf.nn.dropout(h_fc1_relu, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2 = fc_layer(layer_name="fc2", input_tensor=h_fc1_drop, output_dim=256)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2_relu = relu_layer(layer_name="fc2_relu", input_tensor=h_fc2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = fc_layer(layer_name="out_neuron", input_tensor=h_fc2_relu, output_dim=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.reshape(y_conv,[batch_size,1,2]) # y_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef ag_net_3(x_image_batch,keep_prob,batch_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "makes a simple network that can receive 20x20x20 input images. And output 2 classes"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('input'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("input_reshape"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "image batch dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # formally adding one depth dimension to the input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #x_image_batch = tf.reshape(x_image_batch, [batch_size, 20, 20, 20, 2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "input to the first layer dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv1 = conv_layer(layer_name='conv1_5x5x5', input_tensor=x_image_batch, filter_size=[7, 7, 7, 2, 20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu1 = relu_layer(layer_name='relu1', input_tensor=h_conv1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool1 = pool_layer(layer_name='pool1_2x2x2', input_tensor=h_relu1, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv2 = conv_layer(layer_name="conv2_3x3x3", input_tensor=h_pool1, filter_size=[5, 5, 5, 20, 30])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu2 = relu_layer(layer_name="relu2", input_tensor=h_conv2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool2 = pool_layer(layer_name="pool2_2x2x2", input_tensor=h_relu2, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv3 = conv_layer(layer_name="conv3_2x2x2", input_tensor=h_pool2, filter_size=[3, 3, 3, 30, 40])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu3 = relu_layer(layer_name="relu3", input_tensor=h_conv3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool3 = pool_layer(layer_name="pool3_2x2x2", input_tensor=h_relu3, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv4 = conv_layer(layer_name="conv4_2x2x2", input_tensor=h_pool3, filter_size=[3, 3, 3, 40, 50])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu4 = relu_layer(layer_name="relu4", input_tensor=h_conv4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool4 = pool_layer(layer_name="pool4_2x2x2", input_tensor=h_relu4, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv5 = conv_layer(layer_name="conv5_2x2x2", input_tensor=h_pool4, filter_size=[2, 2, 2, 50, 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu5 = relu_layer(layer_name="relu5", input_tensor=h_conv5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool5 = pool_layer(layer_name="pool5_2x2x2", input_tensor=h_relu5, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("flatten_layer"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool2_flat = tf.reshape(h_pool5, [-1, 10 * 10 * 10 * 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1 = fc_layer(layer_name="fc1", input_tensor=h_pool2_flat, output_dim=1024)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1_relu = relu_layer(layer_name="fc1_relu", input_tensor=h_fc1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("dropout"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('dropout_keep_probability', keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1_drop = tf.nn.dropout(h_fc1_relu, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2 = fc_layer(layer_name="fc2", input_tensor=h_fc1_drop, output_dim=256)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2_relu = relu_layer(layer_name="fc2_relu", input_tensor=h_fc2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = fc_layer(layer_name="out_neuron", input_tensor=h_fc2_relu, output_dim=6)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.reshape(y_conv,[batch_size,3,2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass MaxNet:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: write tf file to monitor weights and biases acts123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.w1 = weight_variable([5, 5, 5, 1, 20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.w2 = weight_variable([3, 3, 3, 20, 30])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.w3 = weight_variable([2, 2, 2, 30, 40])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.w4 = weight_variable([2, 2, 2, 40, 50])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.w5 = weight_variable([2, 2, 2, 50, 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.b1 = bias_variable([20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.b2 = bias_variable([30])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.b3 = bias_variable([40])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.b4 = bias_variable([50])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.b5 = bias_variable([60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc1w = weight_variable([7500,1024])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc1b = bias_variable([1024])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc2w = weight_variable([1024,256])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc2b = bias_variable([256])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc3w = weight_variable([256,2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc3b = bias_variable([2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def compute_output(self,image_batch,keep_prob,batch_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        x_image_batch = tf.reshape(image_batch, [batch_size, 20, 20, 20, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_conv1 = tf.nn.conv3d(x_image_batch,self.w1, strides=[1,1,1,1,1], padding='SAME') + self.b1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_relu1 = tf.nn.relu(h_conv1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool1 = tf.nn.max_pool3d(h_relu1,ksize=[1, 2, 2, 2, 1],strides=[1, 2, 2, 2, 1],padding='SAME')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_conv2 = tf.nn.conv3d(h_pool1,self.w2, strides=[1,1,1,1,1], padding='SAME') + self.b2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_relu2 = tf.nn.relu(h_conv2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool2 = tf.nn.max_pool3d(h_relu2, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1], padding='SAME')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_conv3 = tf.nn.conv3d(h_pool2, self.w3, strides=[1, 1, 1, 1, 1], padding='SAME') + self.b3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_relu3 = tf.nn.relu(h_conv3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool3 = tf.nn.max_pool3d(h_relu3, ksize=[1, 1, 1, 1, 1], strides=[1, 1, 1, 1, 1], padding='SAME')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_conv4 = tf.nn.conv3d(h_pool3, self.w4, strides=[1, 1, 1, 1, 1], padding='SAME') + self.b4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_relu4 = tf.nn.relu(h_conv4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool4 = tf.nn.max_pool3d(h_relu4, ksize=[1, 1, 1, 1, 1], strides=[1, 1, 1, 1, 1], padding='SAME')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_conv5 = tf.nn.conv3d(h_pool4, self.w5, strides=[1, 1, 1, 1, 1], padding='SAME') + self.b5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_relu5 = tf.nn.relu(h_conv5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool5 = tf.nn.max_pool3d(h_relu5, ksize=[1, 1, 1, 1, 1], strides=[1, 1, 1, 1, 1], padding='SAME')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool2_flat = tf.reshape(h_pool5, [-1, 5 * 5 * 5 * 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,self.fc1w) + self.fc1b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc2 = tf.nn.relu(tf.matmul(h_fc1_drop, self.fc2w) + self.fc2b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        y_conv = tf.matmul(h_fc2, self.fc3w) + self.fc3b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return y_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#with tf.variable_scope("network"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    max_net = MaxNet()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass ConcatNet:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # variables for concat Graham convolution 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_ll_w1 = weight_variable([11*11*11,2,20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_lp_w1 = weight_variable([11*11*11,2,20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_pp_w1 = weight_variable([11*11*11,2,10])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_pl_w1 = weight_variable([11*11*11,2,10])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_ll_b1 = bias_variable([20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_lp_b1 = bias_variable([20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_pp_b1 = bias_variable([10])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_pl_b1 = bias_variable([10])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pix_size_1 = 0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # self.conc_ll_w2 = weight_variable([11,11,11,200,200])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # self.conc_lp_w2 = weight_variable([11,11,11,150,200])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # self.conc_pp_w2 = weight_variable([11,11,11,100,100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # self.conc_pl_w2 = weight_variable([11,11,11,150,100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # self.conc_ll_b2 = bias_variable([200])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # self.conc_lp_b2 = bias_variable([200])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # self.conc_pp_b2 = bias_variable([100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # self.conc_pl_b2 = bias_variable([100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc1_w = weight_variable([30,100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc1_b = bias_variable([100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc2_w = weight_variable([100,2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc2_b = bias_variable([2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # variables for dense regular convolution123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # internal parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self._cutoffs_xyz_1 = tf.to_float(tf.shape(self.conc_ll_w1))[0:3] * self.pix_size_1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def compute_output(self,lig_elem,lig_coord,rec_elem,rec_coord):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # make the first layer as concat layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # take a few features per atom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # create a sparse tensor with these features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # densify sparse tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # batch image tensor; and put into the dense network123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # put them into dense network123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # *create free energies that can avoid FC layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_elem,rec_coord = af.input.crop_rec_by_lig(lig_coord, rec_elem, rec_coord, pix_size=1, side_pix=20)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ss_pairs, ss_rel_coords = af.geom.pointcloud_pairlist(lig_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 lig_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 cutoffs_xyz=self._cutoffs_xyz_1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 order='NAME',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 keep_null_src=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sd_pairs, sd_rel_coords = af.geom.pointcloud_pairlist(lig_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 rec_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 cutoffs_xyz=self._cutoffs_xyz_1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 order='NAME',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 keep_null_src=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dd_pairs, dd_rel_coords = af.geom.pointcloud_pairlist(rec_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 rec_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 cutoffs_xyz=self._cutoffs_xyz_1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 order='NAME',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 keep_null_src=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ds_pairs, ds_rel_coords = af.geom.pointcloud_pairlist(rec_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 lig_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 cutoffs_xyz=self._cutoffs_xyz_1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 order='NAME',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 keep_null_src=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_feat_0 = tf.to_float(tf.expand_dims(lig_elem, 1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_feat_0 = tf.to_float(tf.expand_dims(rec_elem, 1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_feat_1,d_feat_1 = af.nn.concat_nonlinear_conv3d(s_feat=s_feat_0,d_feat=d_feat_0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                ss_pairs=ss_pairs,sd_pairs=sd_pairs,dd_pairs=dd_pairs,ds_pairs=ds_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                ss_rel_coords=ss_rel_coords,sd_rel_coords=sd_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                dd_rel_coords=dd_rel_coords,ds_rel_coords=ds_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                ss_w=self.conc_ll_w1,sd_w=self.conc_lp_w1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                dd_w=self.conc_pp_w1,ds_w=self.conc_pl_w1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                ss_b=self.conc_ll_b1,sd_b=self.conc_lp_w1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                dd_b=self.conc_pp_b1,ds_b=self.conc_pl_b1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                pix_size=self.pix_size_1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_act_1 = tf.nn.relu(s_feat_1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_act_1 = tf.nn.relu(d_feat_1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # s_feat_2,d_feat_2 = nn_ops.concat_nonlinear_conv3d(s_feat=s_act_1,d_feat=d_act_1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                         ss_pairs=ss_pairs,sd_pairs=sd_pairs,dd_pairs=dd_pairs,ds_pairs=ds_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                         ss_rel_coords=ss_rel_coords,sd_rel_coords=sd_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                         dd_rel_coords=dd_rel_coords,ds_rel_coords=ds_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                         ss_w=self.conc_ll_w2,sd_w=self.conc_lp_w2,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                         dd_w=self.conc_pp_w2,ds_w=self.conc_pl_w2,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                         ss_b=self.conc_ll_b2,sd_b=self.conc_lp_w2,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                         dd_b=self.conc_pp_b2,ds_b=self.conc_pl_b2,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                         pix_size=self.pix_size_1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # s_act_2 = tf.nn.relu(s_feat_2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # d_act_2 = tf.nn.relu(d_feat_2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sum all of the atoms together123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_atomsum = tf.reduce_sum(s_act_1,reduction_indices=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_atomsum = tf.reduce_sum(d_act_1,reduction_indices=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        atomsum = tf.expand_dims(tf.concat([s_atomsum,d_atomsum],0),0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # make two fully connected layers123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1 = tf.nn.relu(tf.matmul(atomsum,self.fc1_w) + self.fc1_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc2 = tf.matmul(h_fc1,self.fc2_w) + self.fc2_b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        return tf.reduce_min(ss_rel_coords) + tf.reduce_min(sd_rel_coords) + tf.reduce_min(dd_rel_coords) + tf.reduce_min(ds_rel_coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return h_fc2[0,:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#with tf.variable_scope("network"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    concat_net = ConcatNet()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF