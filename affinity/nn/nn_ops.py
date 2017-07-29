import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport nn_op_lib123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.c_lib123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef concat_nonlinear_conv3d(k_size,pix_size,w,b,sd_pairs,sd_rel_coords,d_feat,s_feat):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param k_size:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param pix_size:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param d_feat:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param s_feat:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    convout = nn_op_lib._matmul_point_pairs_by_kernel(k_size=k_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                      pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                      w=w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                      sd_pairs=sd_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                      sd_rel_coords=sd_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                      s_feat=s_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                      d_feat=d_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    act = tf.nn.relu(convout+b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    outfeat = tf.segment_sum(act,sd_pairs[:, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef concat_nonlinear_conv3d_v2(k_size,pix_size,s_feat, d_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                               ss_pairs, sd_pairs, dd_pairs, ds_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                               ss_rel_coords, sd_rel_coords, dd_rel_coords, ds_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                               ss_w, sd_w, dd_w, ds_w, ss_b, sd_b, dd_b, ds_b):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param k_size:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param pix_size:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param s_feat:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param d_feat:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ss_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param dd_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ds_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ss_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param dd_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ds_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ss_w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param dd_w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ds_w:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ss_b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param sd_b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param dd_b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param ds_b:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME - requires a more rigorous input parameters check123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: use .get_shape() in place of shape() in the future123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: add options to have a separate central slice123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: assert (kernels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo: activation functions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo test inputs (Exceptions at the time of the convolution)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_ss_conv = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_sd_conv = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_dd_conv = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_ds_conv = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if ss_w is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not (ss_b is None and ss_pairs is None and ss_rel_coords is None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("ss_pairs and ss_rel_coords should be None when ss kernel are None")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        do_ss_conv = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if sd_w is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not (sd_b is None and sd_pairs is None and sd_rel_coords is None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("sd_pairs and sd_rel_coords should be None when sd kernel is None")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        do_ds_conv = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if dd_w is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not (dd_b is None and dd_pairs is None and dd_rel_coords is None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("dd_pairs and dd_rel_coords should be None when dd kernel is None")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        do_dd_conv = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if ds_w is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not (ds_b is None and ds_pairs is None and ds_rel_coords is None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("ds_pairs and ds_rel_coords should be None when ds kernel is None")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        do_ss_conv = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if do_ss_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ss_outfeat = concat_nonlinear_conv3d(k_size=k_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             w=ss_w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             b=ss_b,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             sd_pairs=ss_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             sd_rel_coords=ss_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             s_feat=s_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             d_feat=s_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if do_sd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sd_outfeat = concat_nonlinear_conv3d(k_size=k_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             w=sd_w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             b=sd_b,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             sd_pairs=sd_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             sd_rel_coords=sd_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             s_feat=s_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             d_feat=d_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if do_dd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dd_outfeat = concat_nonlinear_conv3d(k_size=k_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             w=dd_w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             b=dd_b,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             sd_pairs=dd_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             sd_rel_coords=dd_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             s_feat=d_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             d_feat=d_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if do_ds_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ds_outfeat = concat_nonlinear_conv3d(k_size=k_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             pix_size=pix_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             w=ds_w,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             b=ds_b,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             sd_pairs=ds_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             sd_rel_coords=ds_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             s_feat=d_feat,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             d_feat=s_feat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # combine features for the source points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not do_ss_conv and not do_sd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_outfeat = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif not do_ss_conv and do_sd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_outfeat = sd_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif do_ss_conv and not do_sd_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_outfeat = ss_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        s_outfeat = ss_outfeat + sd_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # combine features for the destination points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not do_dd_conv and not do_ds_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_outfeat = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif not do_dd_conv and do_ds_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_outfeat = ds_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    elif do_dd_conv and not do_ds_conv:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_outfeat = dd_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        d_outfeat = dd_outfeat + ds_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return s_outfeat,d_outfeat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atomic_cube_conv3d(src_pairs,dest_pairs,destpnt_rel_coords,src_features,dest_features,ssd_kernel,dsd_kernel,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       ss_kernel=None,sd_kernel=None,ds_kernel=None,dd_kernel=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Backend implementation of the sparse analog of regular 3D convolutions. The two fundamental differences are:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    1) convolutions only happen around the source points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (for dense convolution source point is a cell on a 3D grid with the size pixel_size * stride)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    2) filter is (appears to be) centered on the float coordinates of every source point123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    3) it has separate treatment for source and destination points which are assumed to come from different entities123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Reasons:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    s -> (sd) and d-> (sd) are the normal ways to do computer vision and can capture everything.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # protein-protien-protein can speed up the docking (does not need to be done this way)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        src_pairs: points around which to convolve123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dest_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        destpnt_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        kernel:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Inputs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # ss_kernel sd_kernel ssd_kernel ds_kernel dd_kernel dsd_kernel (this is for pairs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # requirements:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # s -> (s), s -> (d), s -> (sd)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # d -> (s), d -> (d), d -> (sd)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # in case of sd, there are two different independent kernels s_kernel, and d_kernel123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # in all cases num_concat_features * num_output_features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # s-s if used for the ligand only can be very helpful in the future123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # protein featurization can also be complex (and include sequences)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef veawe_module(srcpnt_coords,destpnt_coords,srcpnt_features,destpnt_features,src_pairs,dest_pairs,destpnt_rel_coords,num_neighbors):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        srcpnt_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        destpnt_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        srcpnt_features:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        destpnt_features:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        src_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dest_pairs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        destpnt_rel_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_neighbors:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo assert shape reason123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # todo different variations of cropping the table to num neighbors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_srcpnt = tf.shape(srcpnt_coords)[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_pairs = tf.shape(src_pairs)[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_shape = tf.to_int64(tf.stack([num_neighbors, num_srcpnt]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # if any of the source points has more neighbors than requested, crop them123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_per_srcpnt = tf.segment_sum(tf.ones([num_pairs],tf.int32),src_pairs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_idx = affinity.c_lib.int_sequence.int_sequence(tf.zeros([num_srcpnt], tf.int32), nhbr_per_srcpnt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_fits_table = nhbr_idx < num_neighbors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_idx = tf.boolean_mask(nhbr_idx,nhbr_fits_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    src_pairs = tf.boolean_mask(src_pairs,nhbr_fits_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dest_pairs = tf.boolean_mask(dest_pairs,nhbr_fits_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    destpnt_rel_coords = tf.boolean_mask(destpnt_rel_coords,nhbr_fits_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # convert lists of neighboring points; if some of the points do not have enogh neighbors, pad with 0s123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_indices = tf.concat([tf.to_int64(tf.expand_dims(nhbr_idx,1)),tf.expand_dims(src_pairs,1)],1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    table_values = tf.to_int64(dest_pairs + 1) # shifting coordinates by 1 to allow padding123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_table = tf.SparseTensor(table_indices,table_values, dense_shape=table_shape)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_table = tf.sparse_reorder(nhbr_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nhbr_table = tf.sparse_tensor_to_dense(nhbr_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a 3D table with features from 3D table of neighbors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    empty_feature = tf.zeros([1,tf.shape(destpnt_features)[1]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    destpnt_features = tf.concat([empty_feature,destpnt_features],0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    feature_table = tf.gather(destpnt_features,nhbr_table)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # .... more things to do .......123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return feature_table123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef veawe_input():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Prepares a first layer for the veawe input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feature of distance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feature of atom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feature of atom (one_hot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atomic_convolution_layer(filter_means, filter_stds, radial_filters, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        atom_features, source_atoms, nbr_idx, nbr_atoms, nbr_atoms_mask,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_size=24, atom_types=7, radial_cutoff=12, radial_scaling=1.0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        radial_bias=0.0, neighbors=12):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    distance_matrix = nn_op_lib._compute_feature_distance_matrix(atom_features, nbr_idx, neighbors)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    distances_filtered = nn_op_lib._radial_filter(filter_means, filter_stds, distance_matrix, source_atoms, nbr_atoms, nbr_atoms_mask, atom_types, radial_cutoff, radial_scaling, radial_bias)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    distances_expanded = nn_op_lib._atom_type_one_hot_expansion(distances_filtered, nbr_atoms, atom_types)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #pool along the neighbors dimension123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    distances_pooled = tf.reduce_sum(distances_expanded, axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #flatten the last two dimensions to get features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    feature_matrix = tf.reshape(distances_pooled, shape=[tf.shape(distances_expanded)[0], atom_types * radial_filters])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # #perform normalization on the features123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # mean, var = tf.nn.moments(feature_matrix, axes=[0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # normalized_feature_matrix = tf.nn.batch_normalization(faeture_matrix, mean, var, None, None, 1e-4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return feature_matrix123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atomistic_fc_layer(weights, biases, input_tensor, source_atoms, input_dim, output_dim, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Runs a FC layer by considering each atom's features separately"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    embed_weights = tf.nn.embedding_lookup(params=weights, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    embed_biases = tf.nn.embedding_lookup(params=biases, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    input_tensor = tf.expand_dims(input_tensor, 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    hidden_layer = tf.squeeze(tf.matmul(input_tensor, embed_weights)) + embed_biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    hidden_relu = tf.nn.relu(hidden_layer)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    hidden_drop = tf.nn.dropout(hidden_relu, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return hidden_drop123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atomistic_output_layer(weights, biases, input_tensor, source_atoms, sum_atoms=False):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Runs an output layer by considering each atom's features separately. 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    If sum_atoms is True, it will sum the outputs from each atom.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    If sum_atoms is False, it will take the mean of the outputs from each atom."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    embed_weights = tf.nn.embedding_lookup(params=weights, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    embed_biases = tf.nn.embedding_lookup(params=biases, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    input_tensor = tf.expand_dims(input_tensor, 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    output = tf.squeeze(tf.matmul(input_tensor, embed_weights), axis=2) + embed_biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if sum_atoms:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    	molecule_energy = tf.reduce_sum(output)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    	molecule_energy = tf.reduce_mean(output)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return molecule_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atomic_gather_layer(weights, biases, input_tensor, source_atoms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Takes a weighted sum of each atom's features to get molecular features"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    embed_weights = tf.nn.embedding_lookup(params=weights, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    embed_biases = tf.nn.embedding_lookup(params=biases, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    input_tensor = tf.expand_dims(input_tensor, 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    gather_layer = tf.squeeze(tf.matmul(input_tensor, embed_weights), axis=2) + embed_biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.squeeze(gather_layer)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef molecular_fc_layer(weights, biases, input_tensor):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Actually same as a standard FC layer""" 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    hidden_layer = tf.matmul(input_tensor, weights) + biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    hidden_relu = tf.nn.relu(hidden_layer)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    hidden_drop = tf.nn.dropout(hidden_relu)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return hidden_drop123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef graph_cov_3d():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # graph convolution123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # would it be two points distance only 1 x num_outputs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # two ponts dist + atom type 3 x num outputs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # two points 1000 features each 2001 x num_outputs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feels bad -- distance is nothing special123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # sum(cross product of features x distance x nonlinearity)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # feels bad - does not consider all features of the point123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # 3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # concatenated stick of source and (dest points * 2D kernel * distance)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # is that curve Vijay is painting useful for the network (does gradient descend lead to any reasonable features of the curve) -- test123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # in my case I think that are pairs of features that interact (it's usual to consider all features to be interacting)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # three points123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef graph_conv():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # a real graph convolution123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pass