#!/usr/bin/env python123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# -*- coding: utf-8 -*-123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport importlib123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pwd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport socket123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport urllib123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport zipfile123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom random import randint123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom time import strftime, gmtime123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport requests123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# from PIL import Image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom six.moves import urllib as smurllib123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom constants import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef check_dependencies_installed():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Checks whether the needed dependencies are installed.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return: a list of missing dependencies123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    missing_dependencies = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        import importlib123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except ImportError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        missing_dependencies.append("importlib")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dependencies = ["termcolor",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    "colorama",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    "tensorflow",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    "numpy",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    "PIL",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    "six",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    "tarfile",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    "zipfile",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    "requests"]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for dependency in dependencies:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not can_import(dependency):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            missing_dependencies.append(dependency)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return missing_dependencies123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef can_import(some_module):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Checks whether a module is installed by trying to import it.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param some_module: the name of the module to check123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return: a boolean representing whether the import is successful.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        importlib.import_module(some_module)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except ImportError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef maybe_download_and_extract():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Downloads and extracts the zip from electronneutrino, if necessary"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Nothing to do here if downloads aren't allowed123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not FLAGS.ALLOW_DOWNLOADS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dest_directory = FLAGS.DATA_DIR123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(dest_directory):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.makedirs(dest_directory)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename = FLAGS.DATA_URL.split('/')[-1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filepath = os.path.join(dest_directory, filename)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(filepath):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print_progress_bar(0, 100,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           prefix='Downloading ' + filename + ":", suffix='Complete', length=50,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           fill='█')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def _progress(count, block_size, total_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print_progress_bar(float(count * block_size) / float(total_size) * 100.0, 100,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                               prefix='Downloading ' + filename + ":", suffix='Complete', length=50,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                               fill='█')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        filepath, _ = smurllib.request.urlretrieve(FLAGS.DATA_URL, filepath, _progress)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        statinfo = os.stat(filepath)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    extracted_dir_path = os.path.join(dest_directory, '/images')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(extracted_dir_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        zip_ref = zipfile.ZipFile(filepath, 'r')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        zip_ref.extractall(dest_directory)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        zip_ref.close()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# def verify_dataset():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     Verifies the authenticity of the dataset.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     :raises: Exception if the dataset's images are the wrong size.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     :return: nothing on success123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     which = randint(1, 10000)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     where = os.path.join(FLAGS.DATA_DIR, 'images/%d_L.png' % which)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     im = Image.open(where)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#     width, height = im.size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    # print("w, h: " + str(width) + ", " + str(height))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    if not (width == FLAGS.IMAGE_SIZE and height == FLAGS.IMAGE_SIZE):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        raise Exception("Dataset appears to have been corrupted. (Check " + where + ")")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_time_string():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns the GMT.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return: a formatted string containing the GMT.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_username():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Gets the username of the current user.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return: a string with the username123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return pwd.getpwuid(os.getuid()).pw_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_hostname():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns the hostname of the computer.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return: a string containing the hostname123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return socket.gethostname()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill="█"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Call in a loop to create terminal progress bar. Based on https://stackoverflow.com/a/34325723123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    @params:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        iteration   - Required  : current iteration (Int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        total       - Required  : total iterations (Int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prefix      - Optional  : prefix string (Str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        suffix      - Optional  : suffix string (Str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        decimals    - Optional  : positive number of decimals in percent complete (Int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        length      - Optional  : character length of bar (Int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        fill        - Optional  : bar fill character (Str)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filled_length = int(length * iteration // total)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    bar = fill * filled_length + '-' * (length - filled_length)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix) + '\r')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sys.stdout.flush()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Print New Line on Complete123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if iteration == total:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sys.stdout.write("")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef die(message="", error_code=1):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sys.stderr.write(message)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sys.exit(error_code)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass BColors:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    A class containing ANSI escape sequencing for output formatting.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    HEADER = '\033[95m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    OKBLUE = '\033[94m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    OKGREEN = '\033[92m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    WARNING = '\033[43m\033[30m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FAIL = '\033[91m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ENDC = '\033[0m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    BOLD = '\033[1m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    UNDERLINE = '\033[4m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    MAJORINFO = '\033[93m'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef info(message, source=""):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Print an info message, if necessary.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param message: the message to print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param source: (Optional) prefix to prepend to message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.PRINT_INFO:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if source != "":123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print(BColors.OKBLUE + "[" + source + "]: " + message + "" + BColors.ENDC)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print(BColors.OKBLUE + "" + message + "" + BColors.ENDC)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef printi(message):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Print something in a nice yellow color.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param message: the message to print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(BColors.MAJORINFO + "" + message + "" + BColors.ENDC)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef header(message):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Print a message in a nice purple color.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param message: the message to print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(BColors.HEADER + "" + BColors.BOLD + "" + message + "" + BColors.ENDC)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef ok(message):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Print a message in a nice green color.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param message: the message to print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(BColors.OKGREEN + "" + message + "" + BColors.ENDC)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef warning(message):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Print a message in a nice warning color.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param message: the message to print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(BColors.WARNING + "" + message + "" + BColors.ENDC)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef majorwarning(message):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Print a message in a nice failure color.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param message: the message to print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(BColors.FAIL + "" + "" + message + "" + BColors.ENDC)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef error(message):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Print a message in a nice failure color.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    @alias majorwarning(message)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param message: the message to print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(BColors.FAIL + "" + message + "" + BColors.ENDC)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef check_dataset(data_dir):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Makes sure the dataset seems ok.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param data_dir: the directory with the av4 data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :raises Exception if dataset contains no av4 files123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if len(glob(os.path.join(data_dir + '/**/', "*[_]*.av4"))) == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception("Dataset appears to be empty (looking in " + data_dir + ")")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef rightzpad(string, length):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Pad a string from the right to a given length with zeroes.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param string: the string to pad123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param length: the length to pad to123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return: the padded string123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return (str(string)[::-1]).zfill(length)[::-1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef send_cross_entropy_to_poor_mans_tensorboard(cross_entropy):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    params = {'add': cross_entropy}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    encoded_params = urllib.urlencode(params)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    response = 'No response :('123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.USE_TENSORBOARD:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        response = requests.get(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'https://electronneutrino.com/affinity/poor%20man%27s%20tensorboard/add.php?' + encoded_params)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print (response.status_code)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print (response.content)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return response123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef notify(message, subject="Notification", email=FLAGS.NOTIFICATION_EMAIL):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Send an email with the specified message.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param message: the message to be sent123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param subject: (optional) the subject of the message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param email: (optional) the email to send the message to. Defaults to FLAGS.NOTIFICATION_EMAIL123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return: The response of the server. Should be "Thanks!"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    params = {'message': "[" + get_username() + "@" + get_hostname() + ", " + get_time_string() + "]: " + message,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF              'subject': subject, 'email': email}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    encoded_params = urllib.urlencode(params)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    response = "Emailing blocked by configuration (See constants.py)"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.EMAIL_INFO:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        response = requests.get('https://electronneutrino.com/affinity/notify/notify.php?' + encoded_params)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print (response.status_code)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print (response.content)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return response123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF