class FLAGS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "Dataset info______________________________________________________________________________________________________"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Where the dataset should be stored on the computer.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    DATA_DIR = '../../../images/tmp/images/tmp'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # The URL to get the data from (if it is not found locally)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    DATA_URL = 'https://electronneutrino.com/affinity/shapes/datasets/JSHAPES_360DEG_HARD_50k_200x200.zip'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Whether the testing computer has internet or not123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # (overrides all internet-based actions if set123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # to False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    INTERNET = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Whether to allow the program to download123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # the dataset if it's missing locally123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ALLOW_DOWNLOADS = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # The size of each image in the dataset.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    IMAGE_SIZE = 200123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # The number of classes in the dataset (e.g. 2 for binary classification/JSHAPES, 10 for MNIST/CIFAR, &c.)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    NUM_CLASSES = 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "Training info_____________________________________________________________________________________________________"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Number of examples to load into the training queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    NUM_EXAMPLES_TO_LOAD_INTO_QUEUE = 48000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Number of examples per epoch for training and evaluation123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 9600123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    NUM_EXAMPLES_PER_EPOCH_FOR_EVAL = 4800123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Size of the training batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    BATCH_SIZE = 24123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    USE_FP16 = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    TOWER_NAME = 'tower'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    NUM_THREADS = 255123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    NOTIFICATION_EMAIL = 'andrew2000g+affinity@gmail.com'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    EMAIL_INFO = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    RESTORE = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    RESTORE_FROM = './summaries/'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    LEARNING_RATE = 1e-4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    CHECK_DATASET = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    TRAIN_DIR = './summaries'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    USE_TENSORBOARD = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    KEEP_PROBABILITY = 0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    PRINT_INFO = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # At least 10000 is the standard JSHAPES comparison value123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    MAX_TRAINING_STEPS = 100000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    SEND_LOSS_TO_POOR_MANS_TENSORBOARD_EVERY_N_STEPS = 50123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    SAVE_NETSTATE_AND_EMAIL_STATUS_EVERY_N_STEPS = 1000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF