import tensorflow as tf 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time, sys, os, logging, threading123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom net import AtomicNet123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity as af 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.logging.set_verbosity(tf.logging.DEBUG)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlogging.basicConfig(level=logging.DEBUG)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""gracefully creates directories for the log files and for the network state launches. After that orders network training to start"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsummaries_dir = os.path.join(FLAGS.summaries_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.run_index = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFwhile ((tf.gfile.Exists(summaries_dir + "/"+ str(FLAGS.run_index) +'_train' ) or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index)+'_test' ))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	   or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index) +'_netstate') or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index)+'_logs')) and FLAGS.run_index < 1000:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	FLAGS.run_index += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFelse:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) +'_train' )123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) +'_test')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) +'_netstate')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) +'_logs')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess = tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=8,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF										inter_op_parallelism_threads=8))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcoord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe = af.input.InputPipeVRS1(sess, coord, db_path=FLAGS.database_path, num_threads=FLAGS.num_threads)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_q = input_pipe.self_assemble("lig_coords", "lig_nbr_idx", "lig_nbr_atoms",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"lig_elem", "rec_coords", "rec_nbr_idx", "rec_nbr_atoms", "rec_elem",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"comp_coords", "comp_nbr_idx", "comp_nbr_atoms", "comp_elem", "epoch", "label")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFkeep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFnetwork = AtomicNet(b_size=FLAGS.batch_size, keep_prob=keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFpredicted_energies, b_transit_pars = network.compute_output(input_q)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFepoch = b_transit_pars[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlabels = tf.cast(b_transit_pars[1], tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFl2_loss = (predicted_energies - labels) ** 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFl2_loss_mean = tf.reduce_mean(l2_loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtrain_step_run = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate).minimize(l2_loss_mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#merge all summaries and create a file writer object123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFmerged_summaries = tf.summary.merge_all()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtrain_writer = tf.summary.FileWriter((FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_train"), sess.graph)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#create saver to save and load the network state123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsaver = tf.train.Saver()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif FLAGS.saved_session is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFelse:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print "Restoring variables from sleep. This may take a while..."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	saver.restore(sess, FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.train.start_queue_runners(sess, coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe.start_threads()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.get_default_graph().finalize()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFbatch_num = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFepo = [0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFaverage_loss = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFwhile epo[0] < FLAGS.num_epochs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	epo, loss, _ = sess.run([epoch, l2_loss_mean, train_step_run], feed_dict={keep_prob:0.6})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	average_loss = 0.999 * average_loss + 0.001 * loss123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print 'epo:', epo[0], '  global step:', batch_num, '  average_loss:', '%.4f' % average_loss, '  loss:', '%.4f' % loss, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print '  exps:', '%.2f' % (FLAGS.batch_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	batch_num += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#once in a while save the network state and write variable summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	if (batch_num % 500 == 499):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		summaries = sess.run(merged_summaries, feed_dict={keep_prob:1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		print 'saving to disk...'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		train_writer.add_summary(summaries, batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		saver.save(sess, FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_netstate/saved_state", global_step=batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe.stop_threads()