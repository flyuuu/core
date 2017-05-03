import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass FLAGS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: reformat every part of config to make it suitable to training & testing % evaluations123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """important model parameters"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # GENERAL MODEL PARAMETERS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # size of the 3d pixel to render drug-protein image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pixel_size = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # size of the side of the box (box is centered on ligand's center of mass)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    side_pixels = 20123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # epochs are counted by positive examples123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_epochs = 50000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of background threads per agent on GPU123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_threads = 8123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # batch size for the sampling agent123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_size = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # SAMPLING PARAMETERS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # new positions; exhaustive sampling123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shift_ranges = [9,9,9]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shift_deltas = [3,3,3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial_pose_evals = 50123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # parameters for a single output batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_batch_init_poses = 50123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_batch_gen_poses = 50123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FILE LOCATION PARAMETERS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # path with the training set123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    database_path = "../datasets/unlabeled_av4"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # directory where to write variable/graph summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    summaries_dir = './summaries'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # optional saved session: network from which to load variable states123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saved_session = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # it's a good tradition to name the run with a number (easy to group)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    run_name = '14_test'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TECHNICAL (DO NOT MODIFY) PARAMETERS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # main session for multiagent training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    main_session = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of examples in the database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ex_in_database = None