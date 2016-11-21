# Affinity Core V3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFAffinity core is a starting code for training deep convolutional neural networks on crystallographic images of proteins to predict drug binding. In the simplest case, the training set consists of two sets of structures of complexes of proteins together with small molecules labeled either 1 or 0 (binders and decoys). Networks can be trained to distinguish binders from decoys when given a set of unlabeled ligand-protein structures, and to rank complexes by probability to be strong.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF### scripts:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF[av3_database_master.py](./av3_database_master.py)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcrawls and indexes directoris, parses protein and ligand structures (.pdb files) into numpy (.npy) arrays with 4 columns. The first three columns store the coordinates of all atoms, fourth column stores an atom tag (float) corresponding to a particular element. Hashtable that determines the correspondence between chemical elements and numbers is sourced from [av3_atomdict.py](./av2_atomdict.py). 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFBecause the most commonly used to store molecule structures .pdb format is inherently unstable, some (~0.5%) of the structures may fail to parse. Database master handles the errors in this case. After .npy arrays have been generated, database master creates label-ligand.npy-protein.npy trios and writes them into database_index.csv file. 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFinally, database master reads database_index.csv file, shuffles it and safely splits the data into training and testing sets.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF[av3.py](./av3.py)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFthe main script. Takes database index (train_set.csv), and the database with .npy arrays as an input. Performs training and basic evaluation of the network. Depends on av3_input.py which fills the queue with images. By default, av3 is optimizing weighted cross-entropy for a two-class sclassification problem with FP upweighted 10X compared to FN.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFWhile running, the main script creates directoris with various outputs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF'/summaries/logs' - stores some of the outputs of performance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF'./summaries/netstate' - stores the saved weights of the network123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF'./summaries/test' - stores some of the variable states for visualization in tensorboard 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF'./summaries/train' - stores some of the variable states for visualization in tensorboard 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF[av3_input.py](./av3_input.py)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFgenerates the image queue and fills it with images123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFaffine transform123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcustom filename coordinator class123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFmultiple threads123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF### benchmark:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFWe have tested the 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFCo-crystal structures of proteins and small molecules (binders) can be obtained from [Protein Data Bank](http://www.rcsb.org/).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF