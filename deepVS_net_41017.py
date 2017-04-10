import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom deepVS_input import *123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#---------------------------------HYPERPARAMETERS---------------------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#atom type embedding size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFd_atm = 200123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#amino acid embedding size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFd_amino = 200123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#charge embedding size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFd_chrg = 200123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#distance embedding size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFd_dist = 200123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#number convolutional filters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcf = 400123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#number hidden units123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFh = 50123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#learning rate123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFl = 0.075123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#number of neighbor atoms from ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFk_c = 6123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#number of neighbor atoms from protein123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#k_p = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#number of atom types123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFATOM_TYPES = 7123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#number of distance bins123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFDIST_BINS = 18123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFDIST_INTERVAL = 0.3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#-------------------------------LAYER CONSTRUCTION--------------------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# telling tensorflow how we want to randomly initialize weights123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef weight_variable(shape):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial = tf.truncated_normal(shape, stddev=0.005)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.Variable(initial)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef bias_variable(shape):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial = tf.constant(0.01, shape=shape)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.Variable(initial)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef variable_summaries(var, name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """attaches a lot of summaries to a tensor."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('summaries'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        mean = tf.reduce_mean(var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('mean/' + name, mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('stddev'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('stddev/' + name, stddev)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('max/' + name, tf.reduce_max(var))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar('min/' + name, tf.reduce_min(var))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.histogram(name, var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef embed_layer(layer_name, input, num_atoms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"""transforms the mapped z into feature vectors and returns the resulting tensor"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#input is standard matrix of shape m * k_c * 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#output is tensor of shape k_c * d_atm+d_dist * m123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		with tf.name_scope('atom_weights'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			W_atom = weight_variable([ATOM_TYPES, d_atm])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		with tf.name_scope('dist_weights'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			W_dist = weight_variable([DIST_BINS, d_dist])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	for atom_index in range(len(input)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		for neighbor_index in range(len(input[0])):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			atom_type = input[atom_index][0][0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			dist_bin = input[atom_index][0][1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			if neighbor_index == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				face = tf.concat([tf.gather_nd(W_atom, [[atom_type]]), tf.gather_nd(W_dist, [[dist_bin]])], axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				#get a 1x400 feature embedding for a neighbor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				one_neighbor_features = tf.concat([tf.gather_nd(W_atom, [[atom_type]]), tf.gather_nd(W_dist, [[dist_bin]])], axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				#turns face into k_c * 400123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				face = tf.concat([face, one_neighbor_features], 0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		if atom_index == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			embedded_input = tf.reshape(face, [k_c, d_atm+d_dist, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			#turns embedded input into k_c * 400 * m tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			embedded_input = tf.concat([embedded_input, tf.reshape(face, [k_c, d_atm+d_dist, 1])], 2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#gives embedded_input the depth dimension and batch size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return tf.reshape(embedded_input, [1, k_c, d_atm+d_dist, num_atoms, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef conv_layer(layer_name, input_tensor, filter_size, strides=[1,1,1,1,1], padding='SAME'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"""makes a simple face convolutional layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		with tf.name_scope('weights'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			W_conv = weight_variable(filter_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			variable_summaries(W_conv, layer_name + '/weights')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		with tf.name_scope('biases'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			b_conv = bias_variable([filter_size[3]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			variable_summaries(b_conv, layer_name + '/biases')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		h_conv = tf.nn.conv3d(input_tensor, W_conv, strides=strides, padding=padding) + b_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		tf.summary.histogram(layer_name + '/pooling_output', h_conv)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print layer_name,"output dimensions:", h_conv.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return h_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef pool_layer(layer_name, input_tensor, num_atoms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"""makes a max pool layer that returns the max of each column"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		h_pool = tf.nn.max_pool3d(input_tensor, ksize=[1,1,1,num_atoms,1], strides=[1,1,1,1,1], padding='VALID')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		tf.summary.histogram(layer_name + '/max_pooling_output', h_pool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print layer_name, 'output dimensions:', h_pool.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return h_pool123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef fc_layer(layer_name,input_tensor,output_dim):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"""makes a simple fully connected layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	input_dim = int((input_tensor.get_shape())[1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		weights = weight_variable([input_dim, output_dim])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		variable_summaries(weights, layer_name + '/weights')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	with tf.name_scope('biases'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		biases = bias_variable([output_dim])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		variable_summaries(biases, layer_name + '/biases')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	with tf.name_scope('Wx_plus_b'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		h_fc = tf.matmul(input_tensor, weights) + biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		tf.summary.histogram(layer_name + '/fc_output', h_fc)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print layer_name, "output dimensions:", h_fc.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return h_fc123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#-----------------------------------NETWORK----------------------------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#TODO get ligand_atoms and ligand_coords in the right format123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#Assuming the right input formats to class Z, calling123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#Z().z returns a matrix of usable input data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass Z(object):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def atom_dictionary(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["h"] = 1; ATM["h1"] = 1; ATM["h2"] = 1; ATM["h3"] = 1; ATM["h4"] = 1; ATM["h5"] = 1; ATM["h6"] = 1; ATM["h7"] = 1; ATM["h8"] = 1;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["h1*"] = 1; ATM["h2*"] = 1; ATM["h3*"] = 1; ATM["h4*"] = 1; ATM["h5*"] = 1; ATM["h6*"] = 1; ATM["h7*"] = 1; ATM["h8*"] = 1;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["hg"] = 1; ATM["hxt"] = 1; ATM["hz1"] = 1; ATM["hz2"] = 1; ATM["he2"] = 1; ATM["d"] = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["c"] = 2; ATM["c1"] = 2; ATM["c2"] = 2; ATM["c3"] = 2; ATM["c4"] = 2; ATM["c5"] = 2; ATM["c6"] = 2; ATM["c7"] = 2; ATM["c8"] = 2;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["c1*"] = 2; ATM["c2*"] = 2; ATM["c3*"] = 2; ATM["c4*"] = 2; ATM["c5*"] = 2; ATM["c7*"] = 2; ATM["c8*"] = 2;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["cb"] = 2; ATM["ca"] = 2; ATM["ce"] = 2; ATM["cg"] = 2; ATM["cd"] = 2; ATM["cd1"] = 2; ATM["cd2"] = 2;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["n"] = 3; ATM["n1"] = 3; ATM["n2"] = 3; ATM["n3"] = 3; ATM["n4"] = 3; ATM["n5"] = 3; ATM["n6"] = 3; ATM["n7"] = 3; ATM["n8"] = 3; ATM["nz"] = 3;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["o"] = 4; ATM["o1"] = 4; ATM["o2"] = 4; ATM["o3"] = 4; ATM["o4"] = 4; ATM["o5"] = 4; ATM["o6"] = 4; ATM["o7"] = 4; ATM["o8"] = 4;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["o1*"] = 4; ATM["o2*"] = 4; ATM["o3*"] = 4; ATM["o4*"] = 4; ATM["o5*"] = 4; ATM["o6*"] = 4; ATM["o7*"] = 4; ATM["o8*"] = 4;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["oe1"] = 4; ATM["oe2"] = 4; ATM["cd1"] = 4; ATM["oxt"] = 4;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["f"] = 5; ATM["cl"] = 5; ATM["i"] = 5; ATM["br"] = 5;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["p"] = 6; ATM["s"] = 6; # FIXME S is not really equal to P123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM["b"] = 7; ATM["xx"] = 7; ATM["mg"] = 7; ATM["zn"] = 7; ATM["fe"] = 7; ATM["se"] = 7; ATM["v"] = 7; ATM["sg"] = 7;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ATM['ni'] = 7; ATM['co'] = 7; ATM['as'] = 7; ATM['ru']=7; ATM['mn'] = 7; ATM['mo'] = 7; ATM['re'] = 7; ATM['si'] = 7;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return ATM123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def __init__(self, ligand_atoms, ligand_coords):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            :param ligand_atoms: a set of all atoms in our ligand. in the form of characters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            :param ligand_coords: a dictionary mapping atoms to its coordinate as a tuple. for example "c": (0,0,0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            :param kc: an int - the number of neighbors we want to consider123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.atom_map is a dictionary mapping atoms to an integer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                for example "c": 2. Carbon gets mapped to 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.z is a 3D matrix with dimensions [kc x 2 x m] where m is the total number of atoms in the complex123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                each "face" of the matrix is the kc closest neighbors for an atom A. We have m of these faces - one for each atom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                Each row in a face is [neighbor, distance] - the neighbor to A, and its distance to A123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    we have kc rows in each face.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.ligand_atoms = ligand_atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.ligand_coords = ligand_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.atom_map = self.atom_dictionary()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		self.z = self.build_z()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def convert_coords_to_distances(self, start_atom):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ligand_distances = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		atom_coord = self.ligand_coords[start_atom]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		for neighbor in self.ligand_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			ligand_distances[neighbor] = self.distance(self.ligand_coords[neighbor], atom_coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return ligand_distances123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def distance(self, coord1, coord2):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		x1, y1, z1 = coord1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		x2, y2, z2 = coord2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return ((x1-x2) ** 2 + (y1-y2) ** 2 + (z1-z2) ** 2) ** 0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def get_closest_atoms_and_distances(self, atom):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		distances = self.convert_coords_to_distances(atom)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		closest = {}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		for _ in range(k_c):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			closest_atom = min(distances, key=distances.get)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			closest[closest_atom] = distances[closest_atom]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			del distances[closest_atom]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return closest123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def get_raw_z(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#returns matrix of dimensions [k_c * 2 * m]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		raw_z = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		for atom in self.ligand_atoms:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			kc_neighbors_dict = self.get_closest_atoms_and_distances(atom)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			kc_neighbors_list = [[neighbor, distance] for neighbor, distance in kc_neighbors_dict.items()]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			kc_neighbors_list.sort(key=lambda x: x[1]) #sort by distance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			raw_z.append(kc_neighbors_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return raw_z123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def build_z(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#returns matrix of dimensions [k_c * 2 * m]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		raw_z = self.get_raw_z()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		for atom_index in range(len(raw_z)): #iterate over atoms dimension (m)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			for neighbor_index in range(len(raw_z[0])): #iterate over neighbors (kc)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				atom, distance = raw_z[atom_index][neighbor_index]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				raw_z[atom_index][neighbor_index][0] = self.atom_map[atom]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				raw_z[atom_index][neighbor_index][1] = int(distance//DIST_INTERVAL + 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return raw_z123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef deepVS_net(ligand_atoms, ligand_coords, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#gets a standard array of dimensions m * k_c * 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	input = Z(ligand_atoms, ligand_coords).z123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#do the feature embedding to get a k_c * (d_atm + d_dist) * m TENSOR123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	z = embed_layer('embed_layer', input, len(input))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#convolutional layer - padding = 'VALID' prevents 0 padding123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	z_conv = conv_layer('face_conv', input_tensor=z, filter_size=[k_c, d_atm+d_dist, 1, 1, cf], padding='VALID')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#max pool along the columns (corresponding to each convolutional filter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	z_pool = pool_layer(layer_name='pool_column', input_tensor=z_conv, num_atoms=len(input))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#pool gives us batch*1*1*1*cf tensor; flatten it to get a tensor of length cf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	z_flattened = tf.reshape(z_pool, [-1, cf])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#fully connected layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	z_fc1 = fc_layer(layer_name='fc1', input_tensor=z_flattened, output_dim=h)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#dropout123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#output layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	z_output = fc_layer(layer_name='out_neuron', input_tensor=z_fc1, output_dim=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return z_output123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# print(sess.run(ligand_atoms))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# time.sleep(100)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtligand_atoms = {'h', 'c', 'n', 'o', 'f', 'p', 'b', 'h2'}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtligand_coords = {'h': (0,0,0), 'c': (0,0,1), 'n': (0,2,0), 'o': (1,1,1), 'f': (2,2,3), 'p': (1.5, 1.5, 1.5), 'b': (2,0,0), 'h2': (1,1,1.5)}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtest = deepVS_net(tligand_atoms, tligand_coords, 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint(test)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF