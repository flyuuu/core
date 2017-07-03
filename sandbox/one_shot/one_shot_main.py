import time,os,sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom one_shot_config import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport one_shot_input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append('../../')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport av4_networks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport av4_input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# telling tensorflow how we want to randomly initialize weights123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef train():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "train a network"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # it's better if all of the computations use a single session123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue first123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue, examples_in_database = av4_input.index_the_database_into_q(FLAGS.database_path, shuffle=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create an epoch counter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_counter = tf.Variable(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_counter_increment = tf.assign(batch_counter,tf.Variable(0).count_up_to(np.round((examples_in_database*FLAGS.num_training_epochs)/FLAGS.batch_size)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    epoch_counter = tf.div(batch_counter*FLAGS.batch_size,examples_in_database)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a custom shuffle queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _,current_epoch,_,xyz_label,image_batch = one_shot_input.image_and_label_queue(batch_size=FLAGS.batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                    pixel_size=FLAGS.pixel_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                    side_pixels=FLAGS.side_pixels,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                    num_threads=FLAGS.num_threads,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                    filename_queue=filename_queue,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                    epoch_counter=epoch_counter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("network"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        logits = av4_networks.ag_net_2(image_batch,keep_prob,FLAGS.batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    raw_labels = xyz_label[:,3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    norm_labels = raw_labels/(np.pi)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shuffled_labels = tf.random_shuffle(norm_labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    norm_preds = tf.nn.softmax(tf.reshape(logits, [FLAGS.batch_size, 1, 2]))[:, 0, 1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cost = tf.abs(norm_labels - norm_preds)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cost_mean = tf.reduce_mean(cost)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shuffled_cost_mean = tf.reduce_mean(tf.abs(shuffled_labels-norm_preds))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # optimize the cost of interest123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("optimizer"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        train_step_run = tf.train.AdamOptimizer().minimize(cost_mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # merge all summaries and create a file writer object123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    merged_summaries = tf.summary.merge_all()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_writer = tf.summary.FileWriter((FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_train"), sess.graph)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create saver to save and load the network state123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver = tf.train.Saver(var_list=(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="optimizer")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                     + tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="network")))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.saved_session is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "Restoring variables from sleep. This may take a while..."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        saver.restore(sess,FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # visualization of certain parameters for debugging123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    exmpl_lig_atoms = tf.reduce_sum(tf.cast(image_batch[0,:,:,:,0] >0, tf.float32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    exmpl_rec_atoms = tf.reduce_sum(tf.cast((image_batch[0,:,:,:,1] >0), tf.float32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    exmpl_label = raw_labels[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    exmpl_norm_label = norm_labels[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    exmpl_logit = logits[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    exmpl_norm_pred = norm_preds[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    exmpl_cost = cost[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # launch all threads123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.get_default_graph().finalize()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(sess=sess, coord=coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    np.set_printoptions(precision=3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # training block of the loop123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_num = sess.run(batch_counter_increment)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        epo,my_cost,_ = sess.run([current_epoch,cost_mean,train_step_run],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                     feed_dict={keep_prob: 0.5})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "epoch:",epo[0], "step:", batch_num,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "\tcost:", "%.2f" % my_cost,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "\texps:", "%.2f" % (FLAGS.batch_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # visualization block of the loop123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if (batch_num % 20 == 19):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            my_lig_atoms, my_rec_atoms, my_label,my_norm_label,my_logit,my_norm_pred,my_cost \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                = sess.run([exmpl_lig_atoms,exmpl_rec_atoms,exmpl_label,exmpl_norm_label, exmpl_logit, exmpl_norm_pred, exmpl_cost],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            feed_dict={keep_prob:0.5})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "lig atoms:", my_lig_atoms,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "rec atoms:", my_rec_atoms,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "raw labels:", my_label,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "norm label:", my_norm_label,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "raw logit:", my_logit,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "norm pred:", my_norm_pred,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "cos cost:", my_cost123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            my_cost,my_shuffled_cost = sess.run([cost_mean,shuffled_cost_mean],feed_dict={keep_prob:1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "cost:",my_cost,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "shuffled cost:", my_shuffled_cost123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # network saving block of the loop123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if (batch_num % 1000 == 999):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # once in a while save the network state and write variable summaries to disk123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            summaries = sess.run(merged_summaries, feed_dict={keep_prob: 1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            train_writer.add_summary(summaries, batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            saver.save(sess, FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_netstate/saved_state", global_step=batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#class FLAGS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    """important model parameters"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # size of one pixel generated from protein in Angstroms (float)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    pixel_size = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # size of the box around the ligand in pixels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    side_pixels = 20123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # weights for each class for the scoring function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # number of times each example in the dataset will be read123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    num_epochs = 50000 # epochs are counted based on the number of the protein examples123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # usually the dataset would have multiples frames of ligand binding to the same protein123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # av4_input also has an oversampling algorithm.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # Example: if the dataset has 50 frames with 0 labels and 1 frame with 1 label, and we want to run it for 50 epochs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # 50 * 2(oversampling) * 50(negative samples) = 50 * 100 = 5000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # num_classes = 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # parameters to optimize runs on different machines for speed/performance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # number of vectors(images) in one batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    batch_size = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # number of background processes to fill the queue with images123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    num_threads = 512123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # data directories#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # path to the csv file with names of images selected for training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    database_path = "../../../datasets/labeled_av4"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # directory where to write variable summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    summaries_dir = './summaries'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # optional saved session: network from which to load variable states123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    saved_session = None#'./summaries/2_netstate/saved_state-9999'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main(_):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Create directoris two directories: one for the logs, one for the network state. Start the script.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    summaries_dir = os.path.join(FLAGS.summaries_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FLAGS.run_index defines when123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS.run_index = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS.run_name = FLAGS.run_name + "_one_shot"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index) +'_netstate') \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index)+'_logs'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        FLAGS.run_index += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS.run_name = str(FLAGS.run_index) + "_" + FLAGS.run_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.gfile.MakeDirs(summaries_dir + "/" + FLAGS.run_name +'_netstate')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.gfile.MakeDirs(summaries_dir + "/" + FLAGS.run_name +'_logs')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.app.run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF