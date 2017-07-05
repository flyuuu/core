"""A binary to train CIFAR-10 using a single GPU.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFAccuracy:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcifar10_train.py achieves ~86% accuracy after 100K steps (256 epochs of123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdata) as judged by cifar10_eval.py.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFSpeed: With batch_size 128.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFSystem        | Step Time (sec/batch)  |     Accuracy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF------------------------------------------------------------------123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF1 Tesla K20m  | 0.35-0.60              | ~86% at 60K steps  (5 hours)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF1 Tesla K40m  | 0.25-0.35              | ~86% at 100K steps (4 hours)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFUsage:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFPlease see the tutorial and website for how to download the CIFAR-10123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdata set, compile the program and train the model.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFhttp://tensorflow.org/tutorials/deep_cnn/123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom __future__ import absolute_import123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom __future__ import division123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom __future__ import print_function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom datetime import datetime123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pwd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport simpletrain3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS = tf.app.flags.FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.app.flags.DEFINE_string('train_dir', '/tmp/cifar10_train',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           """Directory where to write event logs """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           """and checkpoint.""")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.app.flags.DEFINE_integer('max_steps', 1000000,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            """Number of batches to run.""")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.app.flags.DEFINE_boolean('log_device_placement', False,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            """Whether to log device placement.""")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.app.flags.DEFINE_integer('log_frequency', 10,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            """How often to log results to the console.""")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef train():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.Graph().as_default():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        global_step = tf.contrib.framework.get_or_create_global_step()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("At train step!!")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print("User name: ", get_username())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if get_username() == 'maksym':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Hi Maksym!")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Get images and labels for CIFAR-10.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Force input pipeline to CPU:0 to avoid operations sometimes ending up on123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # GPU and resulting in a slow down.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # with tf.device('/cpu:0'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        images, labels = simpletrain3.inputs(eval_data=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Build a Graph that computes the logits predictions from the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # inference model.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        logits = simpletrain3.inference(images)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Calculate loss.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        loss = simpletrain3.loss(logits, labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Build a Graph that trains the model with one batch of examples and123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # updates the model parameters.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        train_op = simpletrain3.train(loss, global_step)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        class _LoggerHook(tf.train.SessionRunHook):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            """Logs loss and runtime."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            def begin(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self._step = -1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self._start_time = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            def before_run(self, run_context):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self._step += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return tf.train.SessionRunArgs(loss)  # Asks for loss value.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            def after_run(self, run_context, run_values):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if self._step % FLAGS.log_frequency == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    current_time = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    duration = current_time - self._start_time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self._start_time = current_time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    loss_value = run_values.results123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    examples_per_sec = FLAGS.log_frequency * FLAGS.batch_size / duration123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    sec_per_batch = float(duration / FLAGS.log_frequency)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    format_str = ('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  'sec/batch)')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    print(format_str % (datetime.now(), self._step, loss_value,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                        examples_per_sec, sec_per_batch))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        with tf.train.MonitoredTrainingSession(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                checkpoint_dir=FLAGS.train_dir,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                hooks=[tf.train.StopAtStepHook(last_step=FLAGS.max_steps),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       tf.train.NanTensorHook(loss),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       _LoggerHook()],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                config=tf.ConfigProto(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    log_device_placement=FLAGS.log_device_placement)) as mon_sess:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            while not mon_sess.should_stop():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                mon_sess.run(train_op)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # for _ in range(1000):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #     sess.run(train_op)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main(argv=None):  # pylint: disable=unused-argument123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    simpletrain3.maybe_download_and_extract()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if tf.gfile.Exists(FLAGS.train_dir):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.DeleteRecursively(FLAGS.train_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.gfile.MakeDirs(FLAGS.train_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_username():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return pwd.getpwuid(os.getuid()).pw_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.app.run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF