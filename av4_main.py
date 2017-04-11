import time,os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_input import index_the_database_into_queue,image_and_label_queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_networks import *123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# telling tensorflow how we want to randomly initialize weights123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef train():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "train a network"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # it's better if all of the computations use a single session123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue first123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue, examples_in_database = index_the_database_into_queue(FLAGS.database_path, shuffle=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create an epoch counter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("epoch_counter"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_counter = tf.Variable(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_counter_increment = tf.assign(batch_counter,tf.Variable(0).count_up_to(np.round((examples_in_database*FLAGS.num_epochs)/FLAGS.batch_size)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        epoch_counter = tf.div(batch_counter*FLAGS.batch_size,examples_in_database)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a custom shuffle queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _,current_epoch,label_batch,image_batch = image_and_label_queue(batch_size=FLAGS.batch_size, pixel_size=FLAGS.pixel_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                          side_pixels=FLAGS.side_pixels, num_threads=FLAGS.num_threads,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                          filename_queue=filename_queue, epoch_counter=epoch_counter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    image_batch = tf.sparse_tensor_to_dense(sparse_image_batch,validate_indices=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("network"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        predicted_labels = max_net(image_batch,keep_prob,FLAGS.batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=predicted_labels,labels=label_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy_mean = tf.reduce_mean(cross_entropy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.summary.scalar('cross entropy mean', cross_entropy_mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # randomly shuffle along the batch dimension and calculate an error123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shuffled_labels = tf.random_shuffle(label_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shuffled_cross_entropy_mean = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(predicted_labels,shuffled_labels))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.summary.scalar('shuffled cross entropy mean', shuffled_cross_entropy_mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Adam optimizer is a very heart of the network123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("Adam_optimizer"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        train_step_run = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # merge all summaries and create a file writer object123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    merged_summaries = tf.summary.merge_all()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_writer = tf.summary.FileWriter((FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_train"), sess.graph)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create saver to save and load the network state123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver = tf.train.Saver(var_list=(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,scope="Adam_optimizer") +123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                     tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,scope="network") +123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                     tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,scope="epoch_counter")))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.saved_session is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "Restoring variables from sleep. This may take a while..."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        saver.restore(sess,FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "all variables restored. Start training"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # launch all threads only after the graph is complete and all the variables initialized123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # previously, there was a hard to find occasional problem where the computations would start on unfinished nodes123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # IE: lhs shape [] is different from rhs shape [100] and others123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(sess=sess, coord=coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        print tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        time.sleep(100)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_num = sess.run(batch_counter_increment)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        epo,c_entropy_mean,_ = sess.run([current_epoch,cross_entropy_mean,train_step_run], feed_dict={keep_prob: 0.5})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "epoch:",epo[0],"global step:", batch_num, "\tcross entropy mean:", c_entropy_mean,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "\texamples per second:", "%.2f" % (FLAGS.batch_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if (batch_num % 100 == 99):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # once in a while save the network state and write variable summaries to disk123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            c_entropy_mean,sc_entropy_mean,summaries = sess.run(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                [cross_entropy_mean, shuffled_cross_entropy_mean, merged_summaries], feed_dict={keep_prob: 1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "cross entropy mean:",c_entropy_mean, "shuffled cross entropy mean:", sc_entropy_mean123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            train_writer.add_summary(summaries, batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            saver.save(sess, FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_netstate/saved_state", global_step=batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    assert not np.isnan(cross_entropy_mean), 'Model diverged with loss = NaN'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass FLAGS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """important model parameters"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # size of one pixel generated from protein in Angstroms (float)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pixel_size = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # size of the box around the ligand in pixels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    side_pixels = 20123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # weights for each class for the scoring function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of times each example in the dataset will be read123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_epochs = 50000 # epochs are counted based on the number of the protein examples123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # usually the dataset would have multiples frames of ligand binding to the same protein123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # av4_input also has an oversampling algorithm.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Example: if the dataset has 50 frames with 0 labels and 1 frame with 1 label, and we want to run it for 50 epochs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # 50 * 2(oversampling) * 50(negative samples) = 50 * 100 = 5000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # num_classes = 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # parameters to optimize runs on different machines for speed/performance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of vectors(images) in one batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_size = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of background processes to fill the queue with images123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_threads = 8123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # data directories123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # path to the csv file with names of images selected for training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    database_path = "../datasets/unlabeled_av4"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # directory where to write variable summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    summaries_dir = './summaries'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # optional saved session: network from which to load variable states123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saved_session = None #'./summaries/1_netstate/saved_state-113999'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # main session for multiagent training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    main_session = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main(_):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """gracefully creates directories for the log files and for the network state launches. After that orders network training to start."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    summaries_dir = os.path.join(FLAGS.summaries_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FLAGS.run_index defines when123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS.run_index = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while ((tf.gfile.Exists(summaries_dir + "/"+ str(FLAGS.run_index) +'_train' ) or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index)+'_test' ))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF           or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index) +'_netstate') or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index)+'_logs')) and FLAGS.run_index < 1000:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        FLAGS.run_index += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) +'_train' )123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) +'_test')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) +'_netstate')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) +'_logs')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.app.run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF