#!/usr/bin/env python123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# -*- coding: utf-8 -*-123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom __future__ import print_function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport js_train123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom js_utils import *123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport BACKEND_CONSTANTS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main(argv=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    The main function. It merely sets up the directories and datasets,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    and calls the main training function from `train.py`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Hello, world! v5")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Optionally check dependencies123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if BACKEND_CONSTANTS.CHECK_DEPENDENCIES:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Get a list of missing dependencies123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        missing_dependencies = js_train.check_dependencies_installed()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if len(missing_dependencies) > 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("Not all dependencies are installed! (Missing packages " + ' and '.join(missing_dependencies) +123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            "). See README.md for details.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Say hello to Andrew123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if get_hostname() == "lebennin-vm":123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Привет!")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Download and extract the dataset if it's missing (only on Titan or if specified)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Setting up dataset...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if (get_hostname() == "titan" or FLAGS.CHECK_DATASET) and FLAGS.INTERNET:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        maybe_download_and_extract()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Done.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Run some checks on the dataset to make sure it's correct123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Running tests...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # verify_dataset()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("All tests passed.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Create/clean up directories123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Cleaning up directories...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if tf.gfile.Exists(FLAGS.TRAIN_DIR):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.DeleteRecursively(FLAGS.TRAIN_DIR)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.gfile.MakeDirs(FLAGS.TRAIN_DIR)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.gfile.MakeDirs("summaries/netstate")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Done.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Train the network!!123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    js_train.train(int(argv[1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Welcome to jshapes launcher 4.0.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.app.run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF