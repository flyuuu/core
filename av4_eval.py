import time, os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pandas as pd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_eval_input import image_and_label_queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4 import FLAGS, max_net123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom collections import defaultdict123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.test_set_path = '/home/ubuntu/common/data/new_kaggle/test/unlabeled_av4'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.saved_session = './summaries/3_netstate/saved_state-1199'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.top_k=10123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS.predictions_file_path = re.sub("netstate", "logs", FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass store_predictions:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    store add of the prediction results123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    raw_predictions = defaultdict(list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    processed_predictions = defaultdict(list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def add_batch(self, batch_in_the_range, ligand_file_paths, batch_predictions):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_file_name = map(lambda filename:os.path.basename(filename).split('.')[0],ligand_file_paths)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for in_the_range,ligand,prediction in zip(batch_in_the_range, ligand_file_name, batch_predictions):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if in_the_range:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.raw_predictions[ligand].append(prediction)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def reduce(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if a ligand has more than one predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        use mean as final predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key, value in self.raw_predictions.items():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if len(value) > 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                predictions_size = map(lambda x: len(x), value)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if len(set(predictions_size)) > 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    raise Exception(key, " has different number of predictions ", set(predictions_size))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.processed_predictions[key].append(np.mean(value, axis=0))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.processed_predictions[key].append(value)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def final_predictions(self, predictions_list):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        length = min(len(predictions_list, 10))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return np.mean(predictions_list[:length])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def fill_na(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key in self.raw_predictions.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            value_len = len(self.raw_predictions[key])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if value_len>FLAGS.top_k:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "{} have more predictions than expected, {} reuqired {} found.".format(key,FLAGS.top_k,value_len)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                for i in range(FLAGS.top_k-value_len):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.raw_predictions[key]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save_multiframe_predictions(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key, value in self.raw_predictions.items():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            value_len = len(self.raw_predictions[key])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if value_len>FLAGS.top_k:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "{} have more predictions than expected, {} reuqired {} found.".format(key,FLAGS.top_k,value_len)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                records.append([key]+value[:FLAGS.top_k])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                records.append( [key]+value )123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv = pd.DataFrame(records, columns=['Id']+[ 'Predicted_%d'%i for i in range(1,len(records[0]))])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv.to_csv(FLAGS.predictions_file_path + '_multiframe_submission.csv', index=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save_average(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        take average of multiple predcition123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key,value in self.raw_predictions.items():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            records.append([key,np.mean(np.array(value))])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv = pd.DataFrame(records,columns=['ID','Predicted'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv.to_csv(FLAGS.predictions_file_path+'_average_submission.csv',index=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save_max(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key,value in self.raw_predictions.items():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            records.append([key, np.max(np.array(value))])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv = pd.DataFrame(records, columns=['ID', 'Predicted'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        submission_csv.to_csv(FLAGS.predictions_file_path + '_max_submission.csv', index=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def save(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.save_average()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.save_max()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.save_multiframe_predictions()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef evaluate_on_train_set():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "train a network"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create session which all the evaluation happens in123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    current_epoch, batch_ligand_filename,batch_in_the_range, y_, x_image_batch = image_and_label_queue(sess=sess, batch_size=FLAGS.batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                     pixel_size=FLAGS.pixel_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                     side_pixels=FLAGS.side_pixels,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                     num_threads=FLAGS.num_threads,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                     database_path=FLAGS.test_set_path,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                     num_epochs=FLAGS.num_epochs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    float_image_batch = tf.cast(x_image_batch, tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_size = tf.shape(x_image_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = max_net(float_image_batch, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # compute softmax over raw predictions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    predictions = tf.nn.softmax(y_conv)[:, 1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # restore variables from sleep123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver = tf.train.Saver()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver.restore(sess, FLAGS.saved_session)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(sess=sess, coord=coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a variable to store all predicitons123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    all_predictios = store_predictions()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_num = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "start eval..."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while True or not coord.should_stop():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        test_current_epoch,test_ligand,test_in_the_range ,test_predictions = sess.run([current_epoch,batch_ligand_filename,batch_in_the_range ,predictions],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                              feed_dict={keep_prob: 1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        all_predictios.add_batch(test_in_the_range,test_ligand, test_predictions)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_num += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "batch num", batch_num,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "current epoch"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print test_current_epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if min(test_current_epoch)>FLAGS.top_k:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            break;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord.request_stop()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord.join(threads, stop_grace_period_secs=5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    all_predictios.save()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFevaluate_on_train_set()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint "All Done"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF