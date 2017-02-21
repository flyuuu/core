import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os,time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_utils import generate_deep_affine_transform,affine_transform123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFmultiframe_num = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFmin_frame_in_box = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef index_the_database_into_queue(database_path, shuffle):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Indexes av4 database and returns two lists of filesystem path: ligand files, and protein files.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Ligands are assumed to end with _ligand.av4, proteins should be in the same folders with ligands.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Each protein should have its own folder named similarly to the protein name (in the PDB)."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO controls epochs here123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # for the ligand it's necessary and sufficient to have an underscore in it's name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "number of ligands:", len(glob(os.path.join(database_path + '/**/**/', "*[_]*.av4")))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for ligand_file in glob(os.path.join(database_path + '/**/**/', "*[_]*.av4")):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_file = "/".join(ligand_file.split("/")[:-1]) + "/" + ligand_file.split("/")[-1][:4] + '.av4'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(receptor_file):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ligand_file_list.append(ligand_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            receptor_file_list.append(receptor_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # TODO: remove another naming system from Xiao's scripts                #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            receptor_file = os.path.join(os.path.dirname(ligand_file),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                         os.path.basename(ligand_file).split("_")[0] + '.av4')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if os.path.exists(receptor_file):  # remove later123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                ligand_file_list.append(ligand_file)  #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                receptor_file_list.append(receptor_file)  #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def crystal_path(ligand_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor = os.path.basename(ligand_path).split('_')[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_file_path = os.path.join('/home/ubuntu/xiao/data/newkaggle/dude/crystal/crystal_ligands',receptor,receptor+'_crystal.av4')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return crystal_file_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    crystal_file_list = map(crystal_path,ligand_file_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_list = range(len(ligand_file_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    examples_in_database = len(index_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if examples_in_database == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('av4_input: No files found in the database path:', database_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "Indexed ligand-protein pairs in the database:", examples_in_database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue (tensor) with the names of the ligand and receptors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_tensor = tf.convert_to_tensor(index_list, dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_files = tf.convert_to_tensor(ligand_file_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    crystal_files = tf.convert_to_tensor(crystal_file_list,dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_files = tf.convert_to_tensor(receptor_file_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue = tf.train.slice_input_producer([index_tensor, ligand_files,crystal_files ,receptor_files], num_epochs=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                   shuffle=shuffle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return filename_queue, examples_in_database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef read_receptor_and_multiframe_ligand(filename_queue, epoch_counter):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def decode_av4(serialized_record):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # decode everything into int32123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tmp_decoded_record = tf.decode_raw(serialized_record, tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # first four bytes describe the number of frames in a record123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        number_of_frames = tf.slice(tmp_decoded_record, [0], [1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # labels are saved as int32 * number of frames in the record123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels = tf.slice(tmp_decoded_record, [1], number_of_frames)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # elements are saved as int32 and their number is == to the number of atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        number_of_atoms = ((tf.shape(tmp_decoded_record) - number_of_frames - 1) / (3 * number_of_frames + 1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        elements = tf.slice(tmp_decoded_record, number_of_frames + 1, number_of_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # coordinates are saved as a stack of X,Y,Z where the first(vertical) dimension123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # corresponds to the number of atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # second (horizontal dimension) is x,y,z coordinate of every atom and is always 3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # third (depth) dimension corresponds to the number of frames123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coords_shape = tf.concat(0, [number_of_atoms, [3], number_of_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tmp_coords = tf.slice(tmp_decoded_record, number_of_frames + number_of_atoms + 1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                              tf.shape(tmp_decoded_record) - number_of_frames - number_of_atoms - 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        multiframe_coords = tf.bitcast(tf.reshape(tmp_coords, coords_shape), type=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return labels, elements, multiframe_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    idx = filename_queue[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_file = filename_queue[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    serialized_ligand = tf.read_file(ligand_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    serialized_crystal = tf.read_file(filename_queue[2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    serialized_receptor = tf.read_file(filename_queue[3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_labels, ligand_elements, multiframe_ligand_coords = decode_av4(serialized_ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _,_,crystal_coords = decode_av4(serialized_crystal)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_labels, receptor_elements, multiframe_receptor_coords = decode_av4(serialized_receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # select some frame of ligands, if don't have enough frame, repeat it123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    size = tf.case([(tf.less(multiframe_num,tf.shape(multiframe_ligand_coords)[0]),lambda :tf.shape(multiframe_ligand_coords)[0])],lambda :tf.constant(multiframe_num))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    select_range = tf.range(0, size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    select_frame = tf.mod(select_range,tf.shape(ligand_elements)[0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    multiple_ligand_coords = tf.gather(tf.transpose(multiframe_ligand_coords,perm=[2,0,1]),select_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    labels = tf.gather(ligand_labels,select_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return ligand_file, tf.squeeze(epoch_counter), tf.squeeze(labels), ligand_elements, tf.squeeze(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        multiple_ligand_coords), tf.squeeze(crystal_coords),receptor_elements, tf.squeeze(multiframe_receptor_coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef convert_protein_and_multiple_ligand_to_image(ligand_elements,multiple_lgiand_coords,crystal_ligand_coords,receptor_elements,receptor_coords,side_pixels,pixel_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    max_num_attempts = 1000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    affine_transform_pool_size = 10000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_center_of_mass =tf.reduce_mean(crystal_ligand_coords,reduction_indices=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    centered_crystal_ligand = crystal_ligand_coords - ligand_center_of_mass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    centered_multiple_ligand_coords = multiple_lgiand_coords - ligand_center_of_mass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    centered_receptor_coords = receptor_coords - ligand_center_of_mass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    box_size = (tf.cast(side_pixels, tf.float32)* pixel_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def generate_transition_matrix(attempt, transition_matrix, batch_of_transition_matrices):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transition_matrix = tf.gather(batch_of_transition_matrices,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                      tf.random_uniform([],minval=0,maxval=affine_transform_pool_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                        dtype=tf.int32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        attempt +=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return attempt, transition_matrix,batch_of_transition_matrices123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def not_enough_in_the_box(attempt, transition_matrix, batch_of_transition_matrices,centered_crystal_ligand=centered_crystal_ligand,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           multiple_ligand_coords = centered_multiple_ligand_coords,box_size= box_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           max_num_attempts=max_num_attempts):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def affine_multiple_transform(index,multiple_coordinates=multiple_ligand_coords, transition_matrix=transition_matrix):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            coordinates = tf.gather(multiple_coordinates,index)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            transformed_coordinates,_ = affine_transform(coordinates,transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return transformed_coordinates123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # if crystal ligand in the box123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transformed_crystal_coords,transition_matrix = affine_transform(centered_crystal_ligand,transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        not_all = tf.cast(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tf.reduce_max(tf.cast(tf.square(box_size * 0.5) - tf.square(transformed_crystal_coords) < 0, tf.int32)), tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        within_iteration_limit = tf.cast(tf.reduce_sum(tf.cast(attempt < max_num_attempts, tf.float32)), tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # if docked ligands in the box123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transformed_coords = tf.map_fn(affine_multiple_transform,tf.range(tf.shape(multiple_ligand_coords)[0]),dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # transformed_coords.shape [n_frame,n_atoms,3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # out_of_box_atoms.shape [ n_frame, n_atoms]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        out_of_box_atoms = tf.squeeze(tf.reduce_sum(tf.cast(tf.square(box_size*0.5) - tf.cast(tf.square(transformed_coords),tf.float32)<0,tf.int32),reduction_indices=-1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # out_of_box_frame [n_frame]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        out_of_box_frame = tf.squeeze(tf.cast(tf.reduce_sum(out_of_box_atoms,reduction_indices=-1)>0,tf.int32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        in_the_box_frame = tf.ones(tf.shape(out_of_box_frame),tf.int32) - out_of_box_frame123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return tf.logical_and(tf.logical_and(within_iteration_limit, not_all), tf.less(tf.reduce_sum(in_the_box_frame),multiframe_num))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    attempt = tf.Variable(tf.constant(0,shape=[1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_of_transition_matrices = tf.Variable(generate_deep_affine_transform(affine_transform_pool_size))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    transition_matrix = tf.gather(batch_of_transition_matrices,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  tf.random_uniform([],minval=0,maxval=affine_transform_pool_size,dtype=tf.int64))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    last_attempt, final_transition_matrix, _ = tf.while_loop(not_enough_in_the_box,generate_transition_matrix,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             [attempt,transition_matrix,batch_of_transition_matrices],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             parallel_iterations=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def affine_multiple_transform(index, multiple_coordinates=centered_multiple_ligand_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  transition_matrix=final_transition_matrix):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coordinates = tf.gather(multiple_coordinates, index)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transformed_coordinates, _ = affine_transform(coordinates, transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return transformed_coordinates123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotatated_ligand_coords = tf.map_fn(affine_multiple_transform,tf.range(tf.shape(centered_multiple_ligand_coords)[0]),dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotated_receptor_coords, _ = affine_transform(centered_receptor_coords, final_transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def set_elements_coords_zero(): return  tf.constant([0],dtype=tf.int32),tf.constant([0], dtype=tf.int32), tf.zeros([1,1,3], dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def keep_elements_coords(): return tf.constant([1],dtype=tf.int32), tf.cast(ligand_elements,tf.int32), rotatated_ligand_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    out_of_box_atoms = tf.squeeze(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.reduce_sum(tf.cast(tf.square(box_size * 0.5) - tf.cast(tf.square(rotatated_ligand_coords),tf.float32) < 0, tf.int32),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                      reduction_indices=-1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    out_of_box_frame = tf.squeeze(tf.cast(tf.reduce_sum(out_of_box_atoms, reduction_indices=-1) > 0, tf.int32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    in_the_box_frame = tf.ones(tf.shape(out_of_box_frame),tf.int32) - out_of_box_frame123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # transformed label 1 when rotate success 0 when failed123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    transformed_label,ligand_elements,rotated_ligand_coords = tf.case({tf.greater_equal(tf.reduce_sum(in_the_box_frame),multiframe_num):set_elements_coords_zero},123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                    keep_elements_coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    inbox_ligand_coords = tf.gather(rotated_ligand_coords,in_the_box_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    select_ligand_coords = tf.gather(inbox_ligand_coords,tf.range(multiframe_num))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    epsilon = tf.constant(0.999, dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    half_side_pixels = (side_pixels-1.0)/2.0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    scalar_ligand_coords = tf.cast(select_ligand_coords,tf.float32)/tf.cast(pixel_size,tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ceiled_ligand_coords = tf.cast(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.round((half_side_pixels+scalar_ligand_coords) * epsilon),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.int64)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ceiled_receptor_coords = tf.cast(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.round((tf.constant(-0.5,tf.float32) + (tf.cast(side_pixels, tf.float32) /2.0) + (rotated_receptor_coords / pixel_size)) * epsilon),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.int64)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    top_filter = tf.reduce_max(ceiled_receptor_coords, reduction_indices=1) < side_pixels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    bottom_filter = tf.reduce_min(ceiled_receptor_coords, reduction_indices=1) > 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    retain_atoms = tf.logical_and(top_filter, bottom_filter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cropped_receptor_coords = tf.boolean_mask(ceiled_receptor_coords, retain_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cropped_receptor_elements = tf.boolean_mask(receptor_elements, retain_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    multiple_cropped_receptor_coords = tf.ones([tf.shape(ceiled_ligand_coords)[0],1,1],tf.int64)*cropped_receptor_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_coords = tf.concat(1, [ceiled_ligand_coords, multiple_cropped_receptor_coords])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_elements = tf.concat(0, [ligand_elements + 7, cropped_receptor_elements])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # for each frame assign the 4th dimention as 0,1,2...100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dimention_4th = tf.cast(tf.reshape(tf.range(tf.shape(complex_coords)[0]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                       [tf.shape(complex_coords)[0],1,1]),tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    base = tf.ones([tf.shape(complex_coords)[0],tf.shape(complex_coords)[1],1],tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_frame_depth =tf.cast( dimention_4th*base,tf.int64)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # repeat complex_elements 100 time, used to generate SparseTensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    multiple_complex_elements =tf.reshape( base*tf.reshape(complex_elements,[1,tf.shape(complex_elements)[0],1]),[-1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_coords_4d =tf.reshape( tf.concat(2,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  [complex_coords,ligand_frame_depth]),[-1,4])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sparse_image_4d = tf.SparseTensor(indices=complex_coords_4d,values = multiple_complex_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                      shape=[side_pixels,side_pixels,side_pixels,multiframe_num])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def generate_sparse_image_4d(depth,complex_coords=complex_coords,complex_elements=complex_elements):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        single_complex_coords = tf.gather(complex_coords,depth)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        complex_coords_4d = tf.concat(1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                      [single_complex_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                       tf.reshape(tf.ones(tf.shape(complex_elements),tf.int64)*tf.cast(depth,tf.int64) ,[-1, 1])])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sparse_image_4d = tf.SparseTensor(indices=complex_coords_4d, values=complex_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                          shape=[side_pixels, side_pixels, side_pixels, multiframe_num])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return sparse_image_4d123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   # sparse_images = tf.map_fn(generate_sparse_image_4d,tf.range(tf.shape(complex_coords)[0]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   # sparse_image_4d = tf.sparse_concate(-1,sparse_images)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return sparse_image_4d,ligand_center_of_mass,final_transition_matrix,transformed_label123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef convert_protein_and_ligand_to_image(ligand_elements, multiple_ligand_coords, receptor_elements, receptor_coords, side_pixels,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                        pixel_size,index):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Take coordinates and elements of protein and ligand and convert them into an image.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Return image with one dimension so far."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME abandon ligand when it does not fit into the box (it's kept now)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # max_num_attempts - maximum number of affine transforms for the ligand to be tried123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    max_num_attemts = 1000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # affine_transform_pool_size is the first(batch) dimension of tensor of transition matrices to be returned123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # affine tranform pool is only generated once in the beginning of training and randomly sampled afterwards123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    affine_transform_pool_size = 10000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_coords = tf.gather(multiple_ligand_coords,index)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # transform center ligand around zero123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_center_of_mass = tf.reduce_mean(ligand_coords, reduction_indices=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    centered_ligand_coords = ligand_coords - ligand_center_of_mass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    centered_receptor_coords = receptor_coords - ligand_center_of_mass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # use TF while loop to find such an affine transform matrix that can fit the ligand so that no atoms are outside123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    box_size = (tf.cast(side_pixels, tf.float32) * pixel_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def generate_transition_matrix(attempt, transition_matrix, batch_of_transition_matrices):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """Takes initial coordinates of the ligand, generates a random affine transform matrix and transforms coordinates."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transition_matrix = tf.gather(batch_of_transition_matrices,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                      tf.random_uniform([], minval=0, maxval=affine_transform_pool_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                        dtype=tf.int32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        attempt += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return attempt, transition_matrix, batch_of_transition_matrices123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def not_all_in_the_box(attempt, transition_matrix, batch_of_transition_matrices,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           ligand_coords=centered_ligand_coords, box_size=box_size, max_num_attempts=max_num_attemts):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """Takes affine transform matrix and box dimensions, performs the transformation, and checks if all atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        are in the box."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transformed_coords, transition_matrix = affine_transform(ligand_coords, transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        not_all = tf.cast(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tf.reduce_max(tf.cast(tf.square(box_size * 0.5) - tf.square(transformed_coords) < 0, tf.int32)), tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        within_iteration_limit = tf.cast(tf.reduce_sum(tf.cast(attempt < max_num_attemts, tf.float32)), tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return tf.logical_and(within_iteration_limit, not_all)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    attempt = tf.Variable(tf.constant(0, shape=[1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_of_transition_matrices = tf.Variable(generate_deep_affine_transform(affine_transform_pool_size))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    transition_matrix = tf.gather(batch_of_transition_matrices,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  tf.random_uniform([], minval=0, maxval=affine_transform_pool_size, dtype=tf.int64))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    last_attempt, final_transition_matrix, _ = tf.while_loop(not_all_in_the_box, generate_transition_matrix,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             [attempt, transition_matrix, batch_of_transition_matrices],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                             parallel_iterations=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # rotate receptor and ligand using an affine transform matrix found123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotatated_ligand_coords, _ = affine_transform(centered_ligand_coords, final_transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotated_receptor_coords, _ = affine_transform(centered_receptor_coords, final_transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # check if all of the atoms are in the box, if not set the ligand to 0, but do not raise an error123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def set_elements_coords_zero(): return tf.constant([0], dtype=tf.int32), tf.constant([[0, 0, 0]], dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def keep_elements_coords(): return ligand_elements, rotatated_ligand_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    not_all = tf.cast(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.reduce_max(tf.cast(tf.square(box_size * 0.5) - tf.cast(tf.square(rotatated_ligand_coords),tf.float32) < 0, tf.int32)), tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_elements, rotatated_ligand_coords = tf.case({tf.equal(not_all, tf.constant(True)): set_elements_coords_zero},123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                       keep_elements_coords,exclusive=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    indicate = tf.case({tf.equal(not_all,tf.constant(True)):lambda :tf.constant(True)},lambda :tf.constant(False),exclusive=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # move coordinates of a complex to an integer number so as to put every atom on a grid123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # ceiled coords is an integer number out of real coordinates that corresponds to the index on the cell123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # epsilon - potentially, there might be very small rounding errors leading to additional indexes123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    epsilon = tf.constant(0.999, dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ceiled_ligand_coords = tf.cast(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.round((tf.constant(-0.5,tf.float32) + (tf.cast(side_pixels, tf.float32) /2.0) + (rotatated_ligand_coords / pixel_size)) * epsilon),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.int64)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ceiled_receptor_coords = tf.cast(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.round((tf.constant(-0.5,tf.float32) + (tf.cast(side_pixels, tf.float32) /2.0) + (rotated_receptor_coords / pixel_size)) * epsilon),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.int64)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # crop atoms of the protein that do not fit inside the box123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    top_filter = tf.reduce_max(ceiled_receptor_coords, reduction_indices=1) < side_pixels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    bottom_filter = tf.reduce_min(ceiled_receptor_coords, reduction_indices=1) > 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    retain_atoms = tf.logical_and(top_filter, bottom_filter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cropped_receptor_coords = tf.boolean_mask(ceiled_receptor_coords, retain_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cropped_receptor_elements = tf.boolean_mask(receptor_elements, retain_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # merge protein and ligand together. In this case an arbitrary value of 10 is added to the ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_coords = tf.concat(0, [ceiled_ligand_coords, cropped_receptor_coords])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_elements = tf.concat(0, [ligand_elements + 7, cropped_receptor_elements])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # in coordinates of a protein rounded to the nearest integer can be represented as indices of a sparse 3D tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # values from the atom dictionary can be represented as values of a sparse tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # in this case TF's sparse_tensor_to_dense can be used to generate an image out of rounded coordinates123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # move elemets to the dimension of depth123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_coords_4d = tf.concat(1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  [complex_coords, tf.reshape(tf.ones(tf.shape(complex_elements),dtype=tf.int64)*index, [-1, 1])])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sparse_image_4d = tf.SparseTensor(indices=complex_coords_4d, values=complex_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                      shape=[side_pixels, side_pixels, side_pixels,multiframe_num])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME: try to save an image and see how it looks like123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return sparse_image_4d, ligand_center_of_mass, final_transition_matrix,indicate123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef image_and_label_queue(batch_size, pixel_size, side_pixels, num_threads, filename_queue, epoch_counter):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_file, current_epoch, labels, ligand_elements, multiple_ligand_coords, crystal_coords,receptor_elements, receptor_coords = read_receptor_and_multiframe_ligand(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        filename_queue,epoch_counter=epoch_counter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sparse_image,_,_ ,transformed_label= convert_protein_and_multiple_ligand_to_image(ligand_elements,multiple_ligand_coords,crystal_coords,receptor_elements,receptor_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                           side_pixels,pixel_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    frames = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    masks = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i in range(multiframe_num):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sparse_image,_,_,indicate = convert_protein_and_ligand_to_image(ligand_elements, multiple_ligand_coords, receptor_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                receptor_coords, side_pixels, pixel_size,i)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        frames.append(sparse_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        masks.append(indicate)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #multiframe_batch = tf.boolean_mask(tensor=frames,mask=masks)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #image_4d = tf.sparse_concat(-1,multiframe_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    concate_sparse = lambda :tf.sparse_concate(-1,frames)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    label = tf.cast(tf.equal(tf.reduce_sum(labels),multiframe_num),tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    final_label = label*transformed_label123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return ligand_file,current_epoch,label,sparse_image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #return ligand_file,current_epoch,label,frames,masks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF