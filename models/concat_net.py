import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time,sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append('../av4_utils')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append('../nn')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# FIXME absolute import123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport av4_networks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport av4_input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_config import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfilename_queue, examples_in_database = av4_input.index_the_database_into_q(FLAGS.database_path, shuffle=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFwith tf.variable_scope("epoch_counter"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_counter = tf.Variable(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_counter_increment = tf.assign(batch_counter, tf.Variable(0).count_up_to(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        np.round((examples_in_database * FLAGS.num_training_epochs) / FLAGS.batch_size)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    epoch_counter = tf.div(batch_counter * FLAGS.batch_size, examples_in_database)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFligand_file,epoch_counter,label,lig_elem,lig_coord,rec_elem,rec_coord = av4_input.read_receptor_and_ligand(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue,epoch_counter,lig_frame='OVERSAMPLING')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlogits = av4_networks.concat_net.compute_output(lig_elem=lig_elem,lig_coord=lig_coord,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                rec_elem=rec_elem,rec_coord=rec_coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcoord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFthreads = tf.train.start_queue_runners(sess=sess, coord=coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFwhile True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess.run(logits)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "exps:", "%.3f" % (100 / (time.time() - start))