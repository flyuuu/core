import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os,time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef index_the_database_into_queue(database_path,shuffle):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Indexes av4 database and returns two lists of filesystem path: ligand files, and protein files.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Ligands are assumed to end with _ligand.av4, proteins should be in the same folders with ligands.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Each protein should have its own folder named similarly to the protein name (in the PDB)."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO controls epochs here123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # for the ligand it's necessary and sufficient to have an underscore in it's name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "number of ligands:", len(glob(os.path.join(database_path+'/**/',"*[_]*.av4")))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for ligand_file in glob(os.path.join(database_path+'/**/',"*[_]*.av4")):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_file = "/".join(ligand_file.split("/")[:-1]) + "/" + ligand_file.split("/")[-1][:4] + '.av4'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(receptor_file):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ligand_file_list.append(ligand_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            receptor_file_list.append(receptor_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # TODO: remove another naming system from Xiao's scripts                #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            receptor_file = os.path.join(os.path.dirname(ligand_file),os.path.basename(ligand_file).split("_")[0]+'.av4')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if os.path.exists(receptor_file):                                       # remove later123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                ligand_file_list.append(ligand_file)                                #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                receptor_file_list.append(receptor_file)                            #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_list = range(len(ligand_file_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    examples_in_database = len(index_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if examples_in_database ==0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('av4_input: No files found in the database path:',database_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "Indexed ligand-protein pairs in the database:",examples_in_database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue (tensor) with the names of the ligand and receptors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_tensor = tf.convert_to_tensor(index_list,dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_files = tf.convert_to_tensor(ligand_file_list,dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_files = tf.convert_to_tensor(receptor_file_list,dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue = tf.train.slice_input_producer([index_tensor,ligand_files,receptor_files],num_epochs=None,shuffle=shuffle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return filename_queue,examples_in_database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef read_receptor_and_ligand(filename_queue,epoch_counter,train):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Reads ligand and protein raw bytes based on the names in the filename queue. Returns tensors with coordinates123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    and atoms of ligand and protein for future processing.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Important: by default it does oversampling of the positive examples based on training epoch."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def decode_av4(serialized_record):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # decode everything into int32123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tmp_decoded_record = tf.decode_raw(serialized_record, tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # first four bytes describe the number of frames in a record123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        number_of_frames = tf.slice(tmp_decoded_record, [0], [1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # labels are saved as int32 * number of frames in the record123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels = tf.slice(tmp_decoded_record, [1], number_of_frames)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # elements are saved as int32 and their number is == to the number of atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        number_of_atoms = ((tf.shape(tmp_decoded_record) - number_of_frames - 1) / (3 * number_of_frames + 1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        elements = tf.slice(tmp_decoded_record, number_of_frames + 1, number_of_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # coordinates are saved as a stack of X,Y,Z where the first(vertical) dimension123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # corresponds to the number of atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # second (horizontal dimension) is x,y,z coordinate of every atom and is always 3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # third (depth) dimension corresponds to the number of frames123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coords_shape = tf.concat([number_of_atoms, [3], number_of_frames],0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tmp_coords = tf.slice(tmp_decoded_record, number_of_frames + number_of_atoms + 1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                              tf.shape(tmp_decoded_record) - number_of_frames - number_of_atoms - 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        multiframe_coords = tf.bitcast(tf.reshape(tmp_coords, coords_shape), type=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return labels,elements,multiframe_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # read raw bytes of the ligand and receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    idx = filename_queue[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_file = filename_queue[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    serialized_ligand = tf.read_file(ligand_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    serialized_receptor = tf.read_file(filename_queue[2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # decode bytes into meaningful tensors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_labels, ligand_elements, multiframe_ligand_coords = decode_av4(serialized_ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_labels, receptor_elements, multiframe_receptor_coords = decode_av4(serialized_receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def count_frame_from_epoch(epoch_counter,ligand_labels,train):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """Some simple arithmetics is used to sample all of the available frames123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if the index of the examle is even, positive label is taken every even epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if the index of the example is odd, positive label is taken every odd epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        current negative example increments once every two epochs, and slides along all of the negative examples"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def select_pos_frame(): return tf.constant(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def select_neg_frame(): return tf.mod(tf.div(1+epoch_counter,2), tf.shape(ligand_labels) - 1) +1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        current_frame = tf.cond(tf.equal(tf.mod(epoch_counter + idx + 1, 2), 1), select_pos_frame, select_neg_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        if train==True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        current_frame = tf.cond(tf.equal(tf.mod(epoch_counter+idx+1,2),1),select_pos_frame,select_neg_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#            current_frame = tf.mod(epoch_counter,tf.shape(ligand_labels))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return current_frame123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    current_frame = count_frame_from_epoch(epoch_counter,ligand_labels,train)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_coords = tf.gather(tf.transpose(multiframe_ligand_coords, perm=[2, 0, 1]),current_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    label = tf.gather(ligand_labels,current_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return ligand_file,tf.squeeze(epoch_counter),tf.squeeze(label),ligand_elements,tf.squeeze(ligand_coords),receptor_elements,tf.squeeze(multiframe_receptor_coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef data_and_label_queue(batch_size, num_threads, filename_queue, epoch_counter, train=True):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Creates shuffle queue for training the network"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_file, current_epoch, label, ligand_atoms, ligand_coords, receptor_atoms, receptor_coords = read_receptor_and_ligand(filename_queue, epoch_counter=epoch_counter, train=train)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #consider only the atoms in the binding site123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_atoms, receptor_coords = crop_binding_site(ligand_coords, receptor_atoms, receptor_coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #create the complex by combining the ligand and receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_atoms = tf.concat([ligand_atoms, receptor_atoms], axis=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_coords = tf.concat([ligand_coords, receptor_coords], axis=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    multithread_batch = tf.train.batch([ligand_file, current_epoch, label, ligand_atoms, ligand_coords, receptor_atoms, receptor_coords, complex_atoms, complex_coords],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_size, num_threads=num_threads, capacity=batch_size*3, dynamic_pad=True, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        shapes=[[], [], [], [None], [None, 3], [None], [None, 3], [None], [None, 3]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return multithread_batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Subroutine for data_and_label_queue. Crops around the binding site so that we123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   consider fewer atoms in the receptor for memory purposes.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   RETURNS: (cropped) receptor_atoms, receptor_coords"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef crop_binding_site(ligand_coords, receptor_atoms, receptor_coords):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #transform ligand and receptor atoms around CM123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_cm = tf.reduce_mean(ligand_coords, reduction_indices=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_coords = ligand_coords - ligand_cm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_coords = receptor_coords - ligand_cm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    max_coords = tf.reduce_max(ligand_coords, reduction_indices=0) + 8123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    min_coords = tf.reduce_min(ligand_coords, reduction_indices=0) - 8123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    retain_atoms = tf.logical_and(receptor_coords < max_coords, receptor_coords > min_coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    retain_atoms = tf.reduce_all(retain_atoms, axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    retain_atoms.set_shape(receptor_atoms.shape)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cropped_receptor_coords = tf.boolean_mask(receptor_coords, retain_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cropped_receptor_atoms = tf.boolean_mask(receptor_atoms, retain_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return cropped_receptor_atoms, cropped_receptor_coords