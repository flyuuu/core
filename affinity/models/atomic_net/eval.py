import tensorflow as tf 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time, sys, os, logging, threading123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom net import AtomicNet123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity as af 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.batch_size = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.keep_prob = 1.0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess = tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=8,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF										inter_op_parallelism_threads=8))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcoord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe = af.input.InputPipePDBBind(sess, coord, db_path=FLAGS.test_dir, num_threads=FLAGS.num_threads)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_q = input_pipe.self_assemble("lig_coords", "lig_nbr_idx", "lig_nbr_atoms",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"lig_elem", "rec_coords", "rec_nbr_idx", "rec_nbr_atoms", "rec_elem",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"comp_coords", "comp_nbr_idx", "comp_nbr_atoms", "comp_elem", "epoch", "label")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFkeep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFnetwork = AtomicNet(b_size=FLAGS.batch_size, keep_prob=keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFpredicted_energies, b_transit_pars = network.compute_output(input_q)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFepoch = b_transit_pars[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlabels = tf.cast(b_transit_pars[1], tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFl1_loss = tf.abs(predicted_energies - labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFl1_loss_mean = tf.reduce_mean(l1_loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#create saver to load the network state123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsaver = tf.train.Saver()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif FLAGS.saved_session is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	raise Exception("Must specify a saved session")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFelse:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print "Restoring variables from sleep. This may take a while..."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	saver.restore(sess, FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.train.start_queue_runners(sess, coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe.start_threads()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.get_default_graph().finalize()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtry:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	batch_num = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	epo = [0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	average_loss = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	while epo[0] < 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		loss, l, prediction = sess.run([l1_loss_mean, label, predicted_energies], feed_dict={keep_prob:FLAGS.keep_prob})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		average_loss += loss123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		print 'example number:', batch_num, '  MUE loss:', '%.4f' % loss123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		print '  label:', '%.4f' % l, '\tprediction:', '%.4f' % prediction123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		batch_num += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfinally:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print 'Average mean unsigned error:', '%.4f' % (average_loss/batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	input_pipe.stop_threads()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print 'All done'