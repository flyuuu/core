import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# queue = tf.FIFOQueue(capacity=100, dtypes=[tf.string, tf.string], shapes=[7, 7])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFqueue = tf.FIFOQueue(capacity=100, dtypes=[tf.string, tf.string])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFa = queue.enqueue(["a", "1"])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb = queue.enqueue(["b", "2"])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFqueue.enqueue(["c", "3"])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFqueue.enqueue(["d", "4"])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFqueue.enqueue(["e", "5"])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFqueue.enqueue(["f", "6"])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFqueue.enqueue(["g", "7"])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFqueue.enqueue(["h", "8"])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFk = queue.dequeue()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFl = queue.dequeue()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFwith tf.Session() as sess:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.global_variables_initializer().run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(coord=coord, sess=sess)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i in xrange(1, 3):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sess.run(a)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sess.run(b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("aaa")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print(sess.run([k, l]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print(mk + " " + ml)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF