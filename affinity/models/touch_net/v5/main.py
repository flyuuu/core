import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os,sys,re,time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity as af123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport net123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcoord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe = af.input.InputPipeARS1_DUD_temp(sess,coord,pairlist_dist=3,bindsite_radii=8.66,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             db_path=FLAGS.db_path,num_threads=25,match_prob=0.5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_q = input_pipe.self_assemble("lig_elem","lig_coord","rec_elem","rec_coord",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   "ll_pairs","ll_rel_coords","lr_pairs","lr_rel_coords",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   "rr_pairs","rr_rel_coords","rl_pairs","rl_rel_coords",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   "lig_label","lig_file")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFnetwork = net.CatNet(b_size=10)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFkeep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlaunch = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb_logits,transit_pars = network.compute_output(input_q,keep_prob,launch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb_lig_label = transit_pars[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb_lig_file = transit_pars[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb_cost = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=b_lig_label,logits=b_logits)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcost = tf.reduce_mean(b_cost)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtrain_step_run = tf.train.AdamOptimizer().minimize(cost)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.train.start_queue_runners(sess,coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe.start_threads()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcountzero = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfor b_num in range(1000000):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if b_num < 2000:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        countzero = countzero - 0.0005123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "countzero", countzero123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    my_cost,_ = sess.run([cost,train_step_run],feed_dict={keep_prob:0.5,launch:countzero})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "batch:",b_num,"cost:",my_cost, "exps:", "%.3f" % (FLAGS.b_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if (b_num % 20 == 19):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        my_cost = sess.run([cost],feed_dict={keep_prob:1,launch:0})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "batch:", b_num, "no dropout cost:", my_cost