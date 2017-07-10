import numpy as np 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom constants import CONSTANTS 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#------------------BACK END---------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atomic_convolution_layer(atom_features, source_atoms, nbr_idx, nbr_atoms, nbr_atoms_mask):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def compute_feature_distance_matrix(atom_features, nbr_idx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#atom_features: [B, N, d]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#nbr_idx: [B, N, M]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#gather the corresponding features of the neighbors for each atom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		num_atoms = tf.shape(nbr_idx)[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		batch_pad = tf.convert_to_tensor(range(CONSTANTS.batch_size), dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		batch_pad = tf.reshape(batch_pad, shape=[CONSTANTS.batch_size, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		batch_pad = tf.tile(batch_pad, [1, num_atoms, CONSTANTS.neighbors, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		nbr_idx_for_gather = tf.concat([batch_pad, tf.expand_dims(nbr_idx, 3)], axis=3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		nbr_features = tf.gather_nd(atom_features, nbr_idx_for_gather)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#compute the distance matrix between each atom and neighbor features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		feature_dist = tf.expand_dims(atom_features, axis=2) - nbr_features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		feature_dist = tf.sqrt(tf.reduce_sum(tf.square(feature_dist), axis=3))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return feature_dist123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def radial_filter(distance_matrix, source_atoms, nbr_atoms, atom_mask):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#distance matrix: [B, N, M]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#initialize the filters (with two parameters each - mean and std)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		filter_means = tf.Variable(tf.random_normal(shape=[(CONSTANTS.atom_types+1)**2, CONSTANTS.radial_filters], mean=3.0, stddev=1.5))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		filter_stds = tf.Variable(tf.constant(1.0, shape=[(CONSTANTS.atom_types+1)**2, CONSTANTS.radial_filters]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#TODO: embed the correct filters for each interaction type123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#embed the correct filters - one per source/dest atom type pair123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		param_selector = tf.expand_dims(source_atoms,-1) * (CONSTANTS.atom_types+1) + nbr_atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		embed_means = tf.nn.embedding_lookup(params=filter_means, ids=param_selector)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		embed_stds = tf.nn.embedding_lookup(params=filter_stds, ids=param_selector)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#apply the Gaussian filters to create the corresponding output123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		distance_matrix = tf.expand_dims(distance_matrix, axis=-1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		distances_filtered = tf.exp(-((distance_matrix-embed_means)/embed_stds) ** 2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#apply radial cutoff function and zeros activations for "nonexistent padded atoms"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		distances_filtered *= tf.cos(np.pi * distance_matrix / CONSTANTS.radial_cutoff)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		distances_filtered *= tf.expand_dims(tf.cast(atom_mask, tf.float32), -1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		distances_filtered *= tf.cast(tf.logical_and(distance_matrix > 0, distance_matrix < CONSTANTS.radial_cutoff), tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		distances_filtered = distances_filtered * tf.constant(CONSTANTS.radial_scaling) + tf.constant(CONSTANTS.radial_bias)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return distances_filtered123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def atom_type_one_hot_expansion(distances_filtered, corr_atoms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#distances_filtered: [B, N, M, Nr]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#corr_atoms: [B, N, M]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		atoms_one_hot = tf.expand_dims(tf.one_hot(corr_atoms, CONSTANTS.atom_types+1)[:, :, :, 1:], 3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		distances_expanded = tf.multiply(tf.expand_dims(distances_filtered, -1), atoms_one_hot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return distances_expanded123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distance_matrix = compute_feature_distance_matrix(atom_features, nbr_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distances_filtered = radial_filter(distance_matrix, source_atoms, nbr_atoms, nbr_atoms_mask)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distances_expanded = atom_type_one_hot_expansion(distances_filtered, nbr_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#pool along the neighbors dimension123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distances_pooled = tf.reduce_sum(distances_expanded, axis=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#flatten the last two dimensions to get features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	feature_matrix = tf.reshape(distances_pooled, shape=[CONSTANTS.batch_size, tf.shape(distances_expanded)[1], CONSTANTS.atom_types * CONSTANTS.radial_filters])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#perform batch normalization on the features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	mean, var = tf.nn.moments(feature_matrix, axes=[0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	normalized_feature_matrix = tf.nn.batch_normalization(feature_matrix, mean, var, None, None, 1e-4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return normalized_feature_matrix123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef vijay_fc_layer(input_tensor, source_atoms, input_dim, output_dim, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#input_tensor: [B, N, features]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#embed the correct weights for each atom type123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	weights = tf.Variable(tf.random_normal(shape=[CONSTANTS.atom_types+1, input_dim, output_dim], mean=0.0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	biases = tf.Variable(tf.zeros([CONSTANTS.atom_types+1, output_dim]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_weights = tf.nn.embedding_lookup(params=weights, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_biases = tf.nn.embedding_lookup(params=biases, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	input_tensor = tf.expand_dims(input_tensor, 2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	hidden_layer = tf.squeeze(tf.matmul(input_tensor, embed_weights)) + embed_biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	hidden_relu = tf.nn.relu(hidden_layer)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	hidden_drop = tf.nn.dropout(hidden_relu, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return hidden_drop123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef vijay_output_layer(input_tensor, source_atoms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#input tensor: [B, N, hidden_units]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#embed the correct weights for each atom type123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	weights = tf.Variable(tf.random_normal([CONSTANTS.atom_types+1, CONSTANTS.hidden_units], mean=0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	biases = tf.Variable(tf.zeros([CONSTANTS.atom_types+1, CONSTANTS.hidden_units]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_weights = tf.nn.embedding_lookup(params=weights, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_biases = tf.nn.embedding_lookup(params=biases, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output = tf.multiply(input_tensor, embed_weights) + embed_biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	atomic_energies = tf.reduce_sum(output, axis=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	molecule_energy = tf.reduce_mean(atomic_energies, axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return molecule_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#-----------------FRONT END--------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef vijay_net(ligand_coords, ligand_idx, ligand_atoms, receptor_coords, receptor_idx, receptor_atoms, complex_coords, complex_idx, complex_atoms, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def compute_energy(coords, nbr_idx, nbr_atoms, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		source_atoms = tf.squeeze(nbr_atoms[:, :, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		nbr_idx = nbr_idx[:, :, 1:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		nbr_atoms = nbr_atoms[:, :, 1:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		nbr_atoms_mask = nbr_atoms > 0 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		feature_matrix = atomic_convolution_layer(coords, source_atoms, nbr_idx, nbr_atoms, nbr_atoms_mask)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		for i in range(CONSTANTS.conv_layers - 1):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			feature_matrix = atomic_convolution_layer(feature_matrix, source_atoms, nbr_idx, nbr_atoms, nbr_atoms_mask)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		for i in range(CONSTANTS.fc_layers):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			feature_matrix = vijay_fc_layer(feature_matrix, source_atoms, input_dim=CONSTANTS.atom_types*CONSTANTS.radial_filters, output_dim=CONSTANTS.hidden_units, keep_prob=keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		molecule_energy = vijay_output_layer(feature_matrix, source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		return molecule_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	ligand_energy = compute_energy(ligand_coords, ligand_idx, ligand_atoms, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	receptor_energy = compute_energy(receptor_coords, receptor_idx, receptor_atoms, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	complex_energy = compute_energy(complex_coords, complex_idx, complex_atoms, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	change_energy = complex_energy - ligand_energy - receptor_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return change_energy