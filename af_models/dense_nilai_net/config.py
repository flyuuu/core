import os,re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass FLAGS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """important model parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # GENERAL MODEL PARAMETERS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # size of the 3d pixel to render drug-protein image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pixel_size = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # size of the side of the box (box is centered on ligand's center of mass)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    side_pixels = 20123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # epochs are counted by positive examples123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_epochs = 500123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    eval_epochs = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of background threads per agent on GPU123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_threads = 8123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # batch size for the sampling agent123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_size = 128123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of top frames selected for evaluation123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    eval_top_k = eval_epochs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FILE LOCATION PARAMETERS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    model_home = os.path.dirname(os.path.abspath(__file__))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # path with the training set123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_data_path = os.path.join(model_home ,"../../../datasets/labeled_av4")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    eval_data_path = os.path.join(model_home,'../../../datasets/ordered_unlabeled_av4/')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # directory where to write variable/graph summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    summaries_dir = os.path.join (model_home,'../summaries')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # optional saved session: network from which to load variable states123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_saved_sess = None #'../saved_state-109'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    eval_saved_sess = '../summaries/1_max_net_main_netstate/saved_state-9'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # it's a good tradition to name the run with a number (easy to group)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    run_name = 'max_net'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    predictions_file_path = re.sub("_netstate/", "_eval/", eval_saved_sess)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF