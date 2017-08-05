import numpy as np
import threading
import itertools
import logging
import time
import multiprocessing
import try_lib
import nano_db


logging.basicConfig(level=logging.DEBUG)



db = nano_db.AffinityDB()


arg_ones = np.arange(10000)
arg_twos = np.arange(10000)+10
arg_list = [arg_ones,arg_twos]
db.run_multiprocess(arg_list,"nano_lib.zz.printnumber")
