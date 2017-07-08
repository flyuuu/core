import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append('../')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport nn_op_lib123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef concat_nonlinear_conv3d(s_feat, d_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            ss_pairs, sd_pairs, dd_pairs, ds_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            ss_rel_coords, sd_rel_coords, dd_rel_coords, ds_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            ss_w, sd_w, dd_w, ds_w, ss_b, sd_b, dd_b, ds_b, pix_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param s_feat:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param d_feat:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ss_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param dd_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ds_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ss_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param dd_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ds_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ss_w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param dd_w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ds_w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ss_b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param dd_b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ds_b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param pix_size:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME - requires a more rigorous input parameters check123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: use .get_shape() in place of shape() in the future123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: add options to have a separate central slice123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: assert (kernels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: activation functions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo test inputs (Exceptions at the time of the convolution)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_ss_conv = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_sd_conv = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_dd_conv = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_ds_conv = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if ss_w is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not (ss_b and ss_pairs is None and ss_rel_coords is None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("ss_pairs and ss_rel_coords should be None when ss kernel are None")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        do_ss_conv = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if sd_w is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not (sd_b and sd_pairs is None and sd_rel_coords is None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("sd_pairs and sd_rel_coords should be None when sd kernel is None")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        do_ds_conv = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if dd_w is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not (dd_b and dd_pairs is None and dd_rel_coords is None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("dd_pairs and dd_rel_coords should be None when dd kernel is None")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        do_dd_conv = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if ds_w is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not (ds_b and ds_pairs is None and ds_rel_coords is None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("ds_pairs and ds_rel_coords should be None when ds kernel is None")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        do_ss_conv = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if do_ss_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ss_convout = nn_op_lib._matmul_point_pairs_by_kernel(pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             point_pairs=ss_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             rel_coords=ss_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             kernel=ss_w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             d_features=s_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             s_features=s_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ss_convout = ss_convout + ss_b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ss_act = tf.nn.relu(ss_convout)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ss_outfeat = tf.segment_sum(ss_act, ss_pairs[:, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if do_sd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sd_convout = nn_op_lib._matmul_point_pairs_by_kernel(pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             point_pairs=sd_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             rel_coords=sd_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             kernel=sd_w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             d_features=d_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             s_features=s_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sd_convout = sd_convout + sd_b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sd_act = tf.nn.relu(sd_convout)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sd_outfeat = tf.segment_sum(sd_act, sd_pairs[:, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if do_dd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dd_convout = nn_op_lib._matmul_point_pairs_by_kernel(pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             point_pairs=dd_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             rel_coords=dd_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             kernel=dd_w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             d_features=d_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             s_features=d_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dd_convout = dd_convout + dd_b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dd_act = tf.nn.relu(dd_convout)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dd_outfeat = tf.segment_sum(dd_act, dd_pairs[:, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if do_ds_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ds_convout = nn_op_lib._matmul_point_pairs_by_kernel(pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             point_pairs=ds_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             rel_coords=ds_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             kernel=ds_w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             d_features=s_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             s_features=d_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ds_convout = ds_convout + ds_b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ds_act = tf.nn.relu(ds_convout)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ds_outfeat = tf.segment_sum(ds_act, ds_pairs[:, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # combine features for the source points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not do_ss_conv and not do_sd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_outfeat = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif not do_ss_conv and do_sd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_outfeat = sd_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif do_ss_conv and not do_sd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_outfeat = ss_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_outfeat = ss_outfeat + sd_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # combine features for the destination points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not do_dd_conv and not do_ds_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_outfeat = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif not do_dd_conv and do_ds_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_outfeat = ds_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif do_dd_conv and not do_ds_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_outfeat = dd_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_outfeat = dd_outfeat + ds_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return s_outfeat,d_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atomic_cube_conv3d(src_pairs,dest_pairs,destpnt_rel_coords,src_features,dest_features,ssd_kernel,dsd_kernel,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       ss_kernel=None,sd_kernel=None,ds_kernel=None,dd_kernel=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Backend implementation of the sparse analog of regular 3D convolutions. The two fundamental differences are:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    1) convolutions only happen around the source points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (for dense convolution source point is a cell on a 3D grid with the size pixel_size * stride)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    2) filter is (appears to be) centered on the float coordinates of every source point123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    3) it has separate treatment for source and destination points which are assumed to come from different entities123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Reasons:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    s -> (sd) and d-> (sd) are the normal ways to do computer vision and can capture everything.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # protein-protien-protein can speed up the docking (does not need to be done this way)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        src_pairs: points around which to convolve123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dest_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        destpnt_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        kernel:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Inputs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # ss_kernel sd_kernel ssd_kernel ds_kernel dd_kernel dsd_kernel (this is for pairs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # requirements:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # s -> (s), s -> (d), s -> (sd)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # d -> (s), d -> (d), d -> (sd)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # in case of sd, there are two different independent kernels s_kernel, and d_kernel123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # in all cases num_concat_features * num_output_features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # s-s if used for the ligand only can be very helpful in the future123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # protein featurization can also be complex (and include sequences)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef veawe_module(srcpnt_coords,destpnt_coords,srcpnt_features,destpnt_features,src_pairs,dest_pairs,destpnt_rel_coords,num_neighbors):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        srcpnt_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        destpnt_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        srcpnt_features:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        destpnt_features:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        src_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dest_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        destpnt_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_neighbors:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo assert shape reason123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo different variations of cropping the table to num neighbors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_srcpnt = tf.shape(srcpnt_coords)[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_pairs = tf.shape(src_pairs)[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_shape = tf.to_int64(tf.stack([num_neighbors, num_srcpnt]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # if any of the source points has more neighbors than requested, crop them123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_per_srcpnt = tf.segment_sum(tf.ones([num_pairs],tf.int32),src_pairs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_idx = int_sequence_module.int_sequence(tf.zeros([num_srcpnt], tf.int32), nhbr_per_srcpnt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_fits_table = nhbr_idx < num_neighbors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_idx = tf.boolean_mask(nhbr_idx,nhbr_fits_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    src_pairs = tf.boolean_mask(src_pairs,nhbr_fits_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dest_pairs = tf.boolean_mask(dest_pairs,nhbr_fits_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    destpnt_rel_coords = tf.boolean_mask(destpnt_rel_coords,nhbr_fits_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # convert lists of neighboring points; if some of the points do not have enogh neighbors, pad with 0s123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_indices = tf.concat([tf.to_int64(tf.expand_dims(nhbr_idx,1)),tf.expand_dims(src_pairs,1)],1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_values = tf.to_int64(dest_pairs + 1) # shifting coordinates by 1 to allow padding123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_table = tf.SparseTensor(table_indices,table_values, dense_shape=table_shape)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_table = tf.sparse_reorder(nhbr_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_table = tf.sparse_tensor_to_dense(nhbr_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a 3D table with features from 3D table of neighbors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    empty_feature = tf.zeros([1,tf.shape(destpnt_features)[1]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    destpnt_features = tf.concat([empty_feature,destpnt_features],0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    feature_table = tf.gather(destpnt_features,nhbr_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # .... more things to do .......123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return feature_table123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef veawe_input():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Prepares a first layer for the veawe input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feature of distance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feature of atom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feature of atom (one_hot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef graph_cov_3d():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # graph convolution123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # would it be two points distance only 1 x num_outputs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # two ponts dist + atom type 3 x num outputs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # two points 1000 features each 2001 x num_outputs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feels bad -- distance is nothing special123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # sum(cross product of features x distance x nonlinearity)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feels bad - does not consider all features of the point123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # 3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # concatenated stick of source and (dest points * 2D kernel * distance)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # is that curve Vijay is painting useful for the network (does gradient descend lead to any reasonable features of the curve) -- test123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # in my case I think that are pairs of features that interact (it's usual to consider all features to be interacting)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # three points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef graph_conv():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # a real graph convolution123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF