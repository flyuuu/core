import time, os, sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append('../../../')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity as af123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import CONSTANTS 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef train():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# create a filename queue first123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	filename_queue, examples_in_database = af.input.index_pdbbind_database_into_q(CONSTANTS.database_path, shuffle=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#create an epoch counter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	batch_counter = tf.Variable(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	batch_counter_increment = tf.assign(batch_counter, tf.Variable(0).count_up_to(np.round((examples_in_database*CONSTANTS.num_epochs) / CONSTANTS.batch_size)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	epoch_counter = tf.div(batch_counter * CONSTANTS.batch_size, examples_in_database)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#read data from files123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	_, current_epoch, labels, ligand_coords, ligand_nbr_idx, ligand_nbr_atoms, receptor_coords, receptor_nbr_idx, receptor_nbr_atoms, complex_coords, complex_nbr_idx, complex_nbr_atoms = af.input.data_and_label_queue(CONSTANTS.batch_size, CONSTANTS.num_threads, filename_queue, epoch_counter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#run it through the network123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	vijay_net = af.networks.VijayNet()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	predicted_energies = vijay_net.compute_output(keep_prob, CONSTANTS.batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						ligand_coords, ligand_nbr_idx, ligand_nbr_atoms,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						receptor_coords, receptor_nbr_idx, receptor_nbr_atoms,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF						complex_coords, complex_nbr_idx, complex_nbr_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#calculate the l2_loss123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	labels = tf.bitcast(labels, tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	l2_loss = (predicted_energies - labels) ** 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	l2_loss_mean = tf.reduce_mean(l2_loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	tf.summary.scalar('l2 loss mean', l2_loss_mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#Use adam optimizer to train the network parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	train_step_run = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cross_entropy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#merge all summaries and create a file writer object123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	merged_summaries = tf.summary.merge_all()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	train_writer = tf.summary.FileWriter((CONSTANTS.summaries_dir + '/' + str(CONSTANTS.run_index) + "_train"), sess.graph)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#create saver to save and load the network state123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	saver = tf.train.Saver()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	if CONSTANTS.saved_session is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		print "Restoring variables from sleep. This may take a while..."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		saver.restore(sess, CONSTANTS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#launch all threads after the graph is complete and variables are initialized123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	threads = tf.train.start_queue_runners(sess=sess, coord=coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	tf.get_default_graph().finalize()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		batch_num = sess.run(batch_counter_increment)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		epo, loss, _ = sess.run([current_epoch, l2_loss_mean, train_step_run], feed_dict={keep_prob:CONSTANTS.keep_probability})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		print 'epoch:', epo[0], 'global step:', batch_num, '\tloss:', '%.2f' % loss,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		print '\texps:', '%.2f' % (CONSTANTS.batch_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		#once in a while save the network state and write variable summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		if (batch_num % 500 == 499):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			summaries = sess.run(merged_summaries, feed_dict={keep_prob:1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			print 'saving to disk...'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			train_writer.add_summary(summaries, batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF			saver.save(sess, CONSTANTS.summaries_dir + '/' + str(CONSTANTS.run_index) + "_netstate/saved_state", global_step=batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main(_):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"""gracefully creates directories for the log files and for the network state launches. After that orders network training to start"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	summaries_dir = os.path.join(CONSTANTS.summaries_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# CONSTANTS.run_index defines when123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	CONSTANTS.run_index = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	while ((tf.gfile.Exists(summaries_dir + "/"+ str(CONSTANTS.run_index) +'_train' ) or tf.gfile.Exists(summaries_dir + "/" + str(CONSTANTS.run_index)+'_test' ))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		   or tf.gfile.Exists(summaries_dir + "/" + str(CONSTANTS.run_index) +'_netstate') or tf.gfile.Exists(summaries_dir + "/" + str(CONSTANTS.run_index)+'_logs')) and CONSTANTS.run_index < 1000:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		CONSTANTS.run_index += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		tf.gfile.MakeDirs(summaries_dir + "/" + str(CONSTANTS.run_index) +'_train' )123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		tf.gfile.MakeDirs(summaries_dir + "/" + str(CONSTANTS.run_index) +'_test')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		tf.gfile.MakeDirs(summaries_dir + "/" + str(CONSTANTS.run_index) +'_netstate')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		tf.gfile.MakeDirs(summaries_dir + "/" + str(CONSTANTS.run_index) +'_logs')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	train()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	tf.app.run()