import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom nn_ops import *123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass GraphConv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def __init__(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.keep_prob = 0.6123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.input_dims = 10 #assume the atoms have 10 features each initially123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.conv1_dims = 30123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#initialize the weights/biases for each convolutional layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.conv1_w = tf.Variable(tf.random_normal(shape=[self.input_dims, self.conv1_dims], mean=0.0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.conv1_b = tf.Variable(tf.zeros([self.conv1_dims]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		# TODO: add more convolutional layers123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.hidden_units1 = 128123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#initialize the weights for the FC layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.fc1_w = tf.Variable(tf.random_normal(shape=[self.conv1_dims, self.hidden_units1], mean=0.0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.fc1_b = tf.Variable(tf.zeros([self.hidden_units1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#TODO: add more fully-connected layers123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.out_w = tf.Variable(tf.random_normal(shape=[self.hidden_units1, 2], mean=0.0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.out_b = tf.Variable(tf.zeros([2]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def compute_output(self, adj_matrix, feature_matrix):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#TODO: add more convolutional layers123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		feature_matrix = graph_conv_layer(adj_matrix, feature_matrix, self.conv1_w, self.conv1_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		feature_matrix = graph_max_pool(adj_matrix, feature_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#graph gather: sum all nodes123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		molecular_feats = tf.reduce_sum(feature_matrix, axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#TODO: add more fully-connected layers123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		molecular_feats = fc_layer(molecular_feats, self.fc1_w, self.fc1_b, self.keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		output = tf.matmul(molecular_feats, self.out_w) + self.out_b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return output123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# adj_matrix = tf.ones([24, 100, 100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# feature_matrix = tf.random_normal(shape=[24, 100, 10], mean=0, stddev=0.1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# net = GraphConv()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# output = net.compute_output(adj_matrix, feature_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# result = sess.run(output)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# print result123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# print result.shape