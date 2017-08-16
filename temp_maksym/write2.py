import tensorflow as tf
import numpy as np



def save_record_tfr(filename,cryst_elem,cryst_coord,binders_elem,binders_coordsets,
                    cryst_label,binders_labels,rec_elem,rec_coord):
    """

    :param filename: string (file path to the output file)
    :param pos_per_binder:  integer (number of positions per binder)
    :param cryst_elem: np.array shape=[n_elem] type=float32 (elements of the ligand)
    :param cryst_coord: np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)
    :param binders_elem: list of np.array of shape=[n_elem] type=float32 (elements of binders)
    :param binders_coordsets: list of np.array [n_elem, 3, pos_per_binder] (coordinate sets per each of the bidners)
    :param cryst_label: float32 (something about the crystal pose, like binding affinity)
    :param binders_labels: list of np.array shape=[pos_per_binder] type=float32
    :param rec_elem: np.array of shape [n_elem] of float32
    :param rec_coord: np.array of shape [n_elem, 3]
    :return: None
    """
    # filename
    assert type(filename) == str
    # crystal ligand elements
    assert type(cryst_elem) == np.ndarray
    assert cryst_elem.dtype == np.float32
    assert len(cryst_elem.shape)==1
    # crystal ligand coordinates
    assert type(cryst_coord) == np.ndarray
    assert cryst_coord.dtype == np.float32
    assert len(cryst_coord.shape) == 2
    assert cryst_coord.shape[1]==3
    assert cryst_coord.shape[0]==cryst_elem.shape[0]
    # binders elements
    assert type(binders_elem) == list
    num_binders = len(binders_elem)
    for i in range(num_binders):
        assert type(binders_elem[i]) == np.ndarray
        assert str(binders_elem[i].dtype) in {"float32", "np.float32"}
        assert len(binders_elem[i].shape) == 1
    # binders coordsets
    assert type(binders_coordsets) == list
    assert len(binders_coordsets) == num_binders
    for i in range(num_binders):
        assert type(binders_coordsets[i]) ==np.ndarray
        assert str(binders_coordsets[i].dtype) in {"float32", "np.float32"}
        assert len(binders_coordsets[i].shape) == 3
        assert binders_coordsets[i].shape[2] ==3
        assert binders_coordsets[i].shape[1] == binders_elem[i].shape[0]
    # cryst label
    assert type(cryst_label) == float
    # binders labels
    assert type(binders_labels) == list
    assert len(binders_labels) == num_binders
    for i in range(num_binders):
        assert type(binders_labels[i]) == np.ndarray
        assert str(binders_labels[i].dtype) in {"float32", "np.float32"}
        assert len(binders_labels[i].shape) == 1
        assert binders_labels[i].shape[0] == binders_coordsets[i].shape[0]
    # rec elem
    assert type(rec_elem) == np.ndarray
    assert rec_elem.dtype == np.float32
    assert len(rec_elem.shape) == 1
    # rec coord
    assert type(rec_coord) == np.ndarray
    assert rec_coord.dtype == np.float32
    assert len(rec_coord.shape)==2
    assert rec_coord.shape[1] ==3
    assert rec_coord.shape[0] == rec_elem.shape[0]

    # reshape all of the coordinates into 1d
    _cryst_elem = cryst_elem
    _cryst_coord = cryst_coord.reshape([-1])
    binders_nelem = [binders_elem[i].shape[0] for i in range(num_binders)]
    binders_elemslices = np.concatenate([[0],np.cumsum(binders_nelem)[:-1]])
    _binders_elemslices = np.stack([binders_elemslices,binders_nelem],axis=1).reshape([-1])
    _binders_elem = np.concatenate([binders_elem[i] for i in range(num_binders)],axis=0)
    binders_nframes = [binders_coordsets[i].shape[0] for i in range(num_binders)]
    binders_ncoord = np.array(binders_nelem) * np.array(binders_nframes)
    binders_coordslices = np.concatenate([[0],np.cumsum(binders_ncoord[:-1])])
    _binders_coordslices = np.stack([binders_coordslices,binders_ncoord]).reshape([-1])
    _binders_coordsets = np.concatenate([binders_coordsets[i].reshape([-1]) for i in range(num_binders)])
    _cryst_label = np.asarray([cryst_label],dtype=np.float32)
    _binders_labels = np.concatenate([binders_labels[i].reshape([-1]) for i in range(num_binders)],axis=0)
    _rec_elem = rec_elem
    _rec_coord = rec_coord.reshape([-1])

    # parse the record
    writer = tf.python_io.TFRecordWriter(filename)
    example = tf.train.Example(
        features=tf.train.Features(
        feature={
            '_cryst_elem': tf.train.Feature(float_list=tf.train.FloatList(value=_cryst_elem)),
            '_cryst_coord': tf.train.Feature(float_list=tf.train.FloatList(value=_cryst_coord)),
            '_binders_elemslices': tf.train.Feature(int64_list=tf.train.Int64List(value=_binders_elemslices)),
            '_binders_elem': tf.train.Feature(float_list=tf.train.FloatList(value=_binders_elem)),
            '_binders_coordslices': tf.train.Feature(int64_list=tf.train.Int64List(value=_binders_coordslices)),
            '_binders_coordsets': tf.train.Feature(float_list=tf.train.FloatList(value=_binders_coordsets)),
            '_cryst_label': tf.train.Feature(float_list=tf.train.FloatList(value=_cryst_label)),
            '_binders_labels': tf.train.Feature(float_list=tf.train.FloatList(value=_binders_labels)),
            '_rec_elem': tf.train.Feature(float_list=tf.train.FloatList(value=_rec_elem)),
            '_rec_coord': tf.train.Feature(float_list=tf.train.FloatList(value=_rec_coord)),
             }
         )
    )
    # write the record to disk
    serialized = example.SerializeToString()
    writer.write(serialized)
    writer.close()
    return None



filename = "/home/maksym/Desktop/try_tfr.tfr"

cryst_elem = np.array([1,2,3],dtype=np.float32)

cryst_coord = np.array([[1,1,1],
                        [2,2,2],
                        [3,3,3]],dtype=np.float32)

binders_elem = [np.array([1,1],dtype=np.float32),
                np.array([1,2,3,4],dtype=np.float32)]

binders_coordsets = [np.array([[[1,1,1],[2,2,2]],
                               [[4,4,4],[6,6,6]]],dtype=np.float32),
                     np.array([[[1,1,1],[2,2,2],[4,4,4],[5,5,5]],
                               [[3,3,3],[5,5,5],[6,6,6],[7,7,7]]],dtype=np.float32)]

cryst_label = 0.99
binders_labels = [np.array([0,0.2],dtype=np.float32),np.array([0.3,0.4],dtype=np.float32)]
rec_elem = np.array([1,1,2,5],dtype=np.float32)
rec_coord = np.array([[1,1,1],
                      [2,2,2],
                      [3,3,3],
                      [4,4,4]],dtype=np.float32)

answer = save_record_tfr(filename,cryst_elem,cryst_coord,binders_elem,binders_coordsets,
                cryst_label,binders_labels,rec_elem,rec_coord)

sess = tf.Session()
print answer
#print sess.run(answer)