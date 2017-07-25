import random, time, threading, os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom constants import CONSTANTS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_filename_list(db_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print "Number of (folders) crystal structures:", len(glob(os.path.join(db_path + '/**/')))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	data_files = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	for PDB_folder in glob(os.path.join(db_path + '/**/')):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		data_file = os.path.join(PDB_folder, 'data.npz')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		data_files.append(data_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	examples_in_database = len(data_files)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return data_files, examples_in_database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef launch_enqueue_workers(sess, num_workers, batch_size, database_path, num_epochs):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	1) loads a whole database file into RAM.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	2) creates coordinator and picks protein-ligand-label trios in random order123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	3) creates many workers that collectively pick data from coordinator123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	4) each worker randomly rotates and shifts the box around the ligand center (data augmentation)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	5) each worker converts coordinates(sparse tensor) to image(dense tensor) and enqueues it"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Label = tf.placeholder(dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Ligand_coords = tf.placeholder(dtype=tf.float32, shape=[None, 3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Ligand_nbr_idx = tf.placeholder(dtype=tf.int32, shape=[None, 12])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Ligand_nbr_atoms = tf.placeholder(dtype=tf.int32, shape=[None, 12])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Ligand_elements = tf.placeholder(dtype=tf.int32, shape=[None])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Receptor_coords = tf.placeholder(dtype=tf.float32, shape=[None, 3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Receptor_nbr_idx = tf.placeholder(dtype=tf.int32, shape=[None, 12])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Receptor_nbr_atoms = tf.placeholder(dtype=tf.int32, shape=[None, 12])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Receptor_elements = tf.placeholder(dtype=tf.int32, shape=[None])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Complex_coords = tf.placeholder(dtype=tf.float32, shape=[None, 3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Complex_nbr_idx = tf.placeholder(dtype=tf.int32, shape=[None, 12])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Complex_nbr_atoms = tf.placeholder(dtype=tf.int32, shape=[None, 12])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Complex_elements = tf.placeholder(dtype=tf.int32, shape=[None])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	data_queue = tf.PaddingFIFOQueue(capacity=batch_size*3, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		dtypes=[tf.float32, tf.float32, tf.int32, tf.int32, tf.int32,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						  tf.float32, tf.int32, tf.int32, tf.int32,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						  tf.float32, tf.int32, tf.int32, tf.int32],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		shapes=[[], [None, 3], [None, 12], [None, 12], [None],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF					[None, 3], [None, 12], [None, 12], [None],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF					[None, 3], [None, 12], [None, 12], [None]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	enqueue_op = data_queue.enqueue([Label,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		Ligand_coords, Ligand_nbr_idx, Ligand_nbr_atoms, Ligand_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		Receptor_coords, Receptor_nbr_idx, Receptor_nbr_atoms, Receptor_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		Complex_coords, Complex_nbr_idx, Complex_nbr_atoms, Complex_elements])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	class filename_coordinator_class():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		"""Helps many background processes to read and enqueue data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		1) holds database index123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		2) holds information about which data have been read"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		data_filenames = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		# counter counts the index of the record of numpy array to return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		counter = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		stop = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		num_epochs = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		epoch = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		lock = threading.Lock()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		def load_database_index_file(self, database_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			self.data_filenames, self.num_examples = get_filename_list(database_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		def iterate_one(self, lock=lock):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			with lock:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				data_filename = self.data_filenames[self.counter]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				if (self.num_examples - 1) > self.counter:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF					self.counter += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF					#when the end of file list is reached see if it's the last epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF					if num_epochs > self.epoch:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						self.epoch += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						self.counter = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						print 'training epoch:', self.epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF					else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						#stop the workers123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						self.stop = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						self.counter = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			return data_filename123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	def data_queue_worker(filename_coordinator):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			data_filename = filename_coordinator.iterate_one()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			data = np.load(data_filename)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			ligand_coords = data['ligand_coords']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			ligand_nbr_idx = data['ligand_nbr_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			ligand_nbr_atoms = data['ligand_nbr_atoms']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			ligand_elements = data['ligand_elements']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			receptor_coords = data['receptor_coords']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			receptor_nbr_idx = data['receptor_nbr_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			receptor_nbr_atoms = data['receptor_nbr_atoms']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			receptor_elements = data['receptor_elements']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			complex_coords = data['complex_coords']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			complex_nbr_idx = data['complex_nbr_idx']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			complex_nbr_atoms = data['complex_nbr_atoms']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			complex_elements = data['complex_elements']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			label = data['label'] * -1 * 2.479 / 4.184 # to convert to deltaG123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			sess.run([enqueue_op], feed_dict={Label:label, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				Ligand_coords:ligand_coords, Ligand_nbr_idx:ligand_nbr_idx, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				Ligand_nbr_atoms:ligand_nbr_atoms, Ligand_elements:ligand_elements, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				Receptor_coords:receptor_coords, Receptor_nbr_idx:receptor_nbr_idx, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				Receptor_nbr_atoms:receptor_nbr_atoms, Receptor_elements:receptor_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				Complex_coords:complex_coords, Complex_nbr_idx:complex_nbr_idx, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF				Complex_nbr_atoms:complex_nbr_atoms, Complex_elements:complex_elements})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#load the database index file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	filename_coordinator = filename_coordinator_class()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	filename_coordinator.load_database_index_file(database_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	filename_coordinator.num_epochs = num_epochs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#launch many enqueue workers to fill the queue at the same time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	data_enqueue_threads = [threading.Thread(target=data_queue_worker, args=(filename_coordinator,)) for worker_name in xrange(num_workers)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	for t in data_enqueue_threads:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		print "thread started:",t123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		t.start()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		time.sleep(0.3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return data_queue, filename_coordinator