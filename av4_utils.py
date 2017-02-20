import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# generate one very large tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# take slices from that tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# assuming our tensor is big,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# random slices from it should represent affine transform123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef generate_deep_affine_transform(num_frames):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Generates a very big batch of affine transform matrices in 3D. The first dimension is batch, the other two123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    describe typical affine transform matrices. Deep affine transform can be generated once in the beginning123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    of training, and later slices can be taken from it randomly to speed up the computation."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # shift range is hard coded to 10A because that's how the proteins look like123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # rotation range is hardcoded to 360 degrees123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shift_range = tf.constant(10, dtype=tf.float32)  # FIXME123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotation_range = tf.cast(tf.convert_to_tensor(np.pi * 2), dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # randomly shift along X,Y,Z123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    x_shift = tf.random_uniform([num_frames], minval=-1, maxval=1, dtype=tf.float32) * shift_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_shift = tf.random_uniform([num_frames], minval=-1, maxval=1, dtype=tf.float32) * shift_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    z_shift = tf.random_uniform([num_frames], minval=-1, maxval=1, dtype=tf.float32) * shift_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [1, 0, 0, random_x_shift],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 1, 0, random_y_shift],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 1, random_z_shift],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 0, 1]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # try to do the following:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # generate nine tensors for each of them123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # concatenate and reshape sixteen tensors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_0 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_3 = x_shift123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_1 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_3 = y_shift123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_2 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_3 = z_shift123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_3 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    xyz_shift_stick = tf.pack(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        [afn0_0, afn0_1, afn0_2, afn0_3, afn1_0, afn1_1, afn1_2, afn1_3, afn2_0, afn2_1, afn2_2, afn2_3, afn3_0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF         afn3_1, afn3_2, afn3_3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    xyz_shift_matrix = tf.transpose(tf.reshape(xyz_shift_stick, [4, 4, num_frames]), perm=[2, 0, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # randomly rotate along X123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    x_rot = tf.random_uniform([num_frames], minval=-1, maxval=1, dtype=tf.float32, seed=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                              name=None) * rotation_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [[1, 0, 0, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, cos(x_rot),-sin(x_rot),0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, sin(x_rot),cos(x_rot),0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 0, 1]],dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_0 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_1 = tf.cos(x_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_2 = -tf.sin(x_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_1 = tf.sin(x_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_2 = tf.cos(x_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_3 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    x_rot_stick = tf.pack(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        [afn0_0, afn0_1, afn0_2, afn0_3, afn1_0, afn1_1, afn1_2, afn1_3, afn2_0, afn2_1, afn2_2, afn2_3, afn3_0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF         afn3_1, afn3_2, afn3_3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    x_rot_matrix = tf.transpose(tf.reshape(x_rot_stick, [4, 4, num_frames]), perm=[2, 0, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # randomly rotate along Y123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_rot = tf.random_uniform([num_frames], minval=-1, maxval=1, dtype=tf.float32, seed=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                              name=None) * rotation_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [cos(y_rot), 0,sin(y_rot), 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 1, 0, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [-sin(y_rot), 0,cos(y_rot), 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0 ,0 ,1]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_0 = tf.cos(y_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_2 = tf.sin(y_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_1 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_0 = -tf.sin(y_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_2 = tf.cos(y_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_3 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_rot_stick = tf.pack(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        [afn0_0, afn0_1, afn0_2, afn0_3, afn1_0, afn1_1, afn1_2, afn1_3, afn2_0, afn2_1, afn2_2, afn2_3, afn3_0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF         afn3_1, afn3_2, afn3_3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_rot_matrix = tf.transpose(tf.reshape(y_rot_stick, [4, 4, num_frames]), perm=[2, 0, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # randomly rotate along Z123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    z_rot = tf.random_uniform([num_frames], minval=-1, maxval=1, dtype=tf.float32, seed=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                              name=None) * rotation_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [[cos(z_rot), -sin(z_rot), 0, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [sin(z_rot), cos(z_rot), 0, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 1, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 0, 1]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_0 = tf.cos(z_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_1 = -tf.sin(z_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn0_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_0 = tf.sin(z_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_1 = tf.cos(z_rot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn1_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_2 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn2_3 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_0 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_1 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_2 = tf.zeros([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    afn3_3 = tf.ones([num_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    z_rot_stick = tf.pack(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        [afn0_0, afn0_1, afn0_2, afn0_3, afn1_0, afn1_1, afn1_2, afn1_3, afn2_0, afn2_1, afn2_2, afn2_3, afn3_0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF         afn3_1, afn3_2, afn3_3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    z_rot_matrix = tf.transpose(tf.reshape(z_rot_stick, [4, 4, num_frames]), perm=[2, 0, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    xyz_shift_xyz_rot = tf.matmul(tf.matmul(tf.matmul(xyz_shift_matrix, x_rot_matrix), y_rot_matrix), z_rot_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return xyz_shift_xyz_rot123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef affine_transform(coordinates,transition_matrix):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """applies affine transform to the array of coordinates. By default generates a random affine transform matrix."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coordinates_with_ones = tf.concat(1, [coordinates, tf.cast(tf.ones([tf.shape(coordinates)[0],1]),tf.float32)])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    transformed_coords = tf.matmul(coordinates_with_ones,tf.transpose(transition_matrix))[0:,:-1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return transformed_coords,transition_matrix123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef random_transition_matrix():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    returns a random transition matrix123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotation range - determines random rotations along any of X,Y,Z axis123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shift_range determines allowed shifts along any of X,Y,Z axis123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # shift range is hard coded to 10A because that's how the proteins look like123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # rotation range is hardcoded to 360 degrees123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shift_range = tf.constant(10,dtype=tf.float32) # FIXME123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotation_range = tf.cast(tf.convert_to_tensor(np.pi*2),dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # randomly shift along X,Y,Z123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    x_shift = tf.random_uniform([], minval=-1, maxval=1, dtype=tf.float32)* shift_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_shift = tf.random_uniform([], minval=-1, maxval=1, dtype=tf.float32)* shift_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    z_shift = tf.random_uniform([], minval=-1, maxval=1, dtype=tf.float32)* shift_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [1, 0, 0, random_x_shift],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 1, 0, random_y_shift],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 1, random_z_shift],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 0, 1]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    xyz_shift_matrix = tf.concat(0,[[tf.concat(0,[[1.0],[0.0],[0.0],[x_shift]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[1.0],[0.0],[y_shift]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[0.0],[1.0],[z_shift]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[0.0],[0.0],[1.0]])]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         ])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # randomly rotate along X123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    x_rot = tf.random_uniform([], minval=-1, maxval=1, dtype=tf.float32, seed=None, name=None)*rotation_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [[1, 0, 0, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, cos(x_rot),-sin(x_rot),0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, sin(x_rot),cos(x_rot),0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 0, 1]],dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    x_rot_matrix = tf.concat(0,[[tf.concat(0,[[1.0],[0.0],[0.0],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[tf.cos(x_rot)],[-tf.sin(x_rot)],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[tf.sin(x_rot)],[tf.cos(x_rot)],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[0.0],[0.0],[1.0]])]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         ])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # randomly rotate along Y123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_rot = tf.random_uniform([], minval=-1, maxval=1, dtype=tf.float32, seed=None, name=None) * rotation_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [cos(y_rot), 0,sin(y_rot), 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 1, 0, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [-sin(y_rot), 0,cos(y_rot), 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0 ,0 ,1]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_rot_matrix = tf.concat(0,[[tf.concat(0,[[tf.cos(y_rot)],[0.0],[tf.sin(y_rot)],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[1.0],[0.0],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[-tf.sin(y_rot)],[0.0],[tf.cos(y_rot)],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[0.0],[0.0],[1.0]])]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         ])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    z_rot = tf.random_uniform([], minval=-1, maxval=1, dtype=tf.float32, seed=None, name=None) * rotation_range123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [[cos(z_rot), -sin(z_rot), 0, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [sin(z_rot), cos(z_rot), 0, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 1, 0],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # [0, 0, 0, 1]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    z_rot_matrix = tf.concat(0,[[tf.concat(0,[[tf.cos(z_rot)],[-tf.sin(z_rot)],[0.0],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[tf.sin(z_rot)],[tf.cos(z_rot)],[0.0],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[0.0],[1.0],[0.0]])],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         [tf.concat(0,[[0.0],[0.0],[0.0],[1.0]])]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                         ])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    random_affine_transform_matrix = tf.matmul(tf.matmul(tf.matmul(xyz_shift_matrix,x_rot_matrix),y_rot_matrix),z_rot_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return random_affine_transform_matrix123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# create a tensor of 1000 matrices, concatenate them all123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# try to take a slice of 1 every time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFidx = tf.random_uniform([], minval=0, maxval=100, dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFmany_affine = tf.Variable(tf.pack([random_transition_matrix() for i in range(100)]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#one_tensor = tf.gather(many_affine,idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#one_pix = tf.reduce_max(one_tensor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#multithread_batch = tf.train.batch([one_pix],10,num_threads=1,capacity=40)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinit_op = tf.initialize_all_variables()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess.run(init_op)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcoord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFthreads = tf.train.start_queue_runners(sess,coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint sess.run(many_affine)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    sess.run(multithread_batch) #sess.run(many_affine)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    print "exps:", 10/(time.time()-start)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# print "done"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 25/s per regular slice with one thread123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef affine_transform(coordinates,transition_matrix=random_transition_matrix()):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    applies affine transform to the array of coordinates. By default generates a random affine transform matrix.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coordinates_with_ones = tf.concat(1, [coordinates, tf.cast(tf.ones([tf.shape(coordinates)[0],1]),tf.float32)])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    transformed_coords = tf.matmul(coordinates_with_ones,tf.transpose(transition_matrix))[0:,:-1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return transformed_coords,transition_matrix"""