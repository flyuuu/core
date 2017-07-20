#!/usr/bin/env python123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# -*- coding: utf-8 -*-123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFMain file for js_train123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport js123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom js_utils import *123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef train():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Make logging very verbose123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.logging.set_verbosity(tf.logging.DEBUG)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.Session(config=tf.ConfigProto(log_device_placement=False,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                          operation_timeout_in_ms=600000)) as sess:  # Stop after 10 minutes123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Get images and labels for MSHAPES123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Setting up getting batches and labels")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        filequeue, images_batch, labels_batch = js.inputs(eval_data=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Got two batches")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Image batch shape: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print(images_batch.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Labels batch shape:")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print(labels_batch.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Create a global step variable.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # This is sometimes needed for training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # (e.g. variable weight decay)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        global_step = tf.contrib.framework.get_or_create_global_step()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Build a Graph that computes the logits predictions from the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # inference model.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # logits = js.inference(images_batch)  # Naive method123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        logits = js.combined_stm_net(images_batch)  # Actual method123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Calculate loss.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        loss = js.loss(logits, labels_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Build a Graph that trains the model with one batch of examples and123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # updates the model parameters.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        train_op = js.train(loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Set up session saver/loader123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        saver = tf.train.Saver(var_list=(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Restore from session, if necessary123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.RESTORE:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Restoring...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            saver = tf.train.Saver()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            saver.restore(sess, FLAGS.RESTORE_FROM)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Restored.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # If not restoring variables, initialize them123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Initializing global variables")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # tf.set_random_seed(42)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tf.global_variables_initializer().run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Finished")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Start the training coorinator and the queue runners123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Starting coordinator and queue runners")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        threads = tf.train.start_queue_runners(coord=coord, sess=sess)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Ok")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # tf.group(enqueues, reenqueues)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # enqueue everything as needed123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # e = sess.run([enqueues])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print("Enqueue result ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print(e)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # queue_size = sess.run(filequeue.size())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print("Initial queue size: " + str(queue_size))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Run training for a certain number of steps123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i in xrange(0, FLAGS.MAX_TRAINING_STEPS):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # Run the training operaion, and get the loss123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            _, my_loss = sess.run([train_op, loss])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # Do some formatting magic on the loss by storing it as an array123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ml = np.array(my_loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # Report the step and the cross-entropy loss123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print('Step: %d     Cross entropy loss: % 6.2f' % (i, ml))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # Send the cross-entropy to the knock-off tensorboard every ~50 steps123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if i % FLAGS.SEND_LOSS_TO_POOR_MANS_TENSORBOARD_EVERY_N_STEPS == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                send_cross_entropy_to_poor_mans_tensorboard(str(ml))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # Every ~1000 steps, save the results and send an email123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if i % FLAGS.SAVE_NETSTATE_AND_EMAIL_STATUS_EVERY_N_STEPS == 0 and i != 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                # Send informative email via νe123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                notify("Current cross-entropy loss: " + str(ml) + ".", subject="Running stats [step " + str(i) + "]")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                # Save the current net state123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                saver.save(sess, "summaries/netstate/saved_state", global_step=i)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # If the loss is not a number, stop training and send an email123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if np.isnan(ml):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print("Oops")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                notify("Diverged :(", subject="Process ended")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                sys.exit(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Finished training")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Finish off the filename queue coordinator.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Requesting thread stop")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coord.request_stop()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Ok")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Joining threads")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coord.join(threads)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Ok")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Finished")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF