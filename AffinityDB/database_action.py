"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFProcessing data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport re 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport subprocess123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom functools import partial123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom utils import log, smina_param, timeit, count_lines123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#import openbabel123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport prody123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport config123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import data_dir123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom db_v2 import AffinityDatabase123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom parse_binding_DB import read_PDB_bind123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdb = AffinityDatabase()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _makedir(path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.makedirs(path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef download(table_idx, param, input_data):                                                                                    # todo (maksym) remove all datums123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:                                                                                                                # folder = output_folder123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor = input_data                                                                                                # datum = pdb_id123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = param['output_folder']                                                                                        # papram = params123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder_name = '{}_{}'.format(table_idx, output_folder)                                                                  # todo: sn == idx (everywhere)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dest_dir = os.path.join(data_dir, output_folder_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _makedir(dest_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pdb_path = os.path.join(dest_dir, receptor+'.pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not os.path.exists(pdb_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            download_address = 'https://files.rcsb.org/download/{}.pdb'.format(receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.system('wget -P {} {}'.format(dest_dir, download_address))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        header = prody.parsePDBHeader(pdb_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = [receptor, header['experiment'], header['resolution'], 1, 'success']                                     # datum = success report123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)                                                                                       # db.insert(success_report)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = [input_data, 'unk', 0, 0, str(e)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef split_ligand(table_idx, param, input_data):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if type(input_data).__name__ in ['tuple', 'list']:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            input_data = input_data[0]                                                                                            # do not allow x = x[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor = input_data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        fit_box_size = param['fit_box_size']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = param['output_folder']                                                                                        # which folder ? output_folder123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = '{}_{}'.format(table_idx, output_folder)                                                                       # all table_sn become table_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_download_folder = param['input_download_folder']                                                                      # rename all these into standard "source folder"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pdb_dir = os.path.join(data_dir, input_download_folder)                                                               # download_folder = source_folder123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pdb_path = os.path.join(pdb_dir, receptor+'.pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parsed_pdb = prody.parsePDB(pdb_path)                                                                               # parsed = parsed_pdb123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parsed_header = prody.parsePDBHeader(pdb_path)                                                                         # parsed123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_lig_dir = os.path.join(data_dir, output_folder, receptor)                                                              # data_dir as not an argument of the function (should come as an argument)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _makedir(output_lig_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligands = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for chem in parsed_header['chemicals']:                                                               # ligands = ligands_in_pdb123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ligands.append([chem.chain, str(chem.resnum), chem.resname])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for chain, resnum, resname in ligands:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                lig = parsed_pdb.select('chain {} resnum {}'.format(chain, resnum))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                heavy_lig = lig.select('not hydrogen')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                heavy_atom = heavy_lig.numAtoms()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                heavy_coord =heavy_lig.getCoords()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                max_size_on_axis = max(heavy_coord.max(axis=0) - heavy_coord.min(axis=0))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                lig_name = '_'.join([receptor,chain,resnum,resname,'ligand']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                prody.writePDB(os.path.join(output_lig_dir, lig_name), lig)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                record = [receptor, chain, resnum, resname, heavy_atom, max_size_on_axis, 1, 'success']                                     # data = success_message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                record =  [receptor, chain, resnum, resname, 0, 0, 0, str(e)]                                                # data = failure_message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception(str(e))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef split_receptor(table_idx, param, datum):                                                                             # param = params;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:                                                                                                                # datum = pdb_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if type(datum).__name__ in ['tuple','list']:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            datum = datum[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor = datum                                                                                                # receptor = pdb_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = param['output_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = '{}_{}'.format(table_idx, output_folder)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_download_folder = param['input_download_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_pdb_dir = os.path.join(data_dir,input_download_folder)                                                                # pdb_dir = input_dir123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_pdb_path = os.path.join(input_pdb_dir, receptor+'.pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parsed_pdb = prody.parsePDB(input_pdb_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parsed_header = prody.parsePDBHeader(input_pdb_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_rec_dir = os.path.join(data_dir, output_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _makedir(output_rec_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligands = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for chem in parsed_header['chemicals']:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            chain, resnum, resname = chem.chain, chem.resnum, chem.resname123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ligands.append([chain, str(resnum), resname])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for chain, resnum, resname in ligands:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                rec = parsed_pdb.select('not (chain {} resnum {})'.format(chain, resnum))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                rec = rec.select('not water')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                heavy_atom = rec.select('not hydrogen').numAtoms()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                rec_name = '_'.join([receptor, chain, resnum, resname, 'receptor']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                prody.writePDB(os.path.join(output_rec_dir, rec_name), rec)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                record = [receptor, chain, resnum, resname, heavy_atom, parsed_header['experiment'], parsed_header['resolution'] , 1 , 'success'] # datum = success_message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                record = [receptor, chain, resnum, resname, 0, 0, str(e)]                                                # datum = failure_message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                db.insert(table_idx, records) 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception(str(e))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef reorder(table_idx, param, input_data):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor, chain, resnum, resname = input_data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = param['output_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = '{}_{}'.format(table_idx, output_folder)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_lig_folder = param['input_ligand_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_folder = param['input_receptor_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        smina_pm = smina_param()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        smina_pm.param_load(param['smina_param'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        out_dir = os.path.join(data_dir, output_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _makedir(out_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        out_name = '_'.join(input_data + ['ligand']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        out_path = os.path.join(out_dir, out_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_lig_dir = os.path.join(data_dir, input_lig_folder, receptor)                                                         # lig_dir = input_lig_dir123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_name = '_'.join(input_data + ['ligand']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_lig_path = os.path.join(input_lig_dir, lig_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_dir = os.path.join(data_dir, input_rec_folder, receptor)                                                          # rec_dir = input_rec_dir123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_name = '_'.join(input_data + ['receptor']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_path = os.path.join(input_rec_dir, rec_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        kw = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'receptor': input_rec_path,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'ligand': input_lig_path,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'autobox_ligand':input_lig_path,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'out':out_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cmd = smina_pm.make_command(**kw)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print cmd                                                                                                       # print "smina parameters for reordering:', cmd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cl.wait()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prody.parsePDB(out_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = input_data + [1, 'success']                                                                                 # datum = success_message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = input_data + [0, str(e)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef smina_dock(table_idx, param, input_data):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor, chain, resnum, resname = input_data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = param['output_folder']                                                                                        # folder = output_folder123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        output_folder = '{}_{}'.format(table_idx, output_folder)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_lig_folder = param['input_ligand_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_folder = param['input_receptor_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        smina_pm = smina_param()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        smina_pm.param_load(param['smina_param'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        out_dir = os.path.join(data_dir, output_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _makedir(out_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        out_name = '_'.join(input_data + ['ligand']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        out_path = os.path.join(out_dir, out_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_lig_dir = os.path.join(data_dir, input_lig_folder , receptor)                                                         # lig_dir = input_lig_dir123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_name = '_'.join(input_data + ['ligand']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_lig_path = os.path.join(input_lig_dir, lig_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_dir = os.path.join(data_dir, input_rec_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_name = '_'.join(input_data + ['receptor']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_path = os.path.join(input_rec_dir, rec_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        kw = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'receptor': input_rec_path,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'ligand': input_lig_path,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'autobox_ligand':input_lig_path,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'out':out_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cmd = smina_pm.make_command(**kw)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print cmd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cl.wait()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prody.parsePDB(out_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = input_data + [1, 'success']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = input_data + [0, str(e)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef overlap(table_idx, param, input_data):                                                                                    # a prticularly bad datum123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor, chain, resnum, resname = input_data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_folder = param['input_docked_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_folder = param['input_crystal_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        clash_cutoff_A = param['clash_cutoff_A']                                                                        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #clash_size_cutoff                                                                                              # make sure we compute a real number123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_name = '_'.join([receptor, chain, resnum, resname, 'ligand']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_dir = os.path.join(data_dir, input_docked_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_path = os.path.join(input_docked_dir, lig_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_dir = os.path.join(data_dir, input_crystal_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_path = os.path.join(input_crystal_dir, lig_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_coords = prody.parsePDB(input_docked_path).getCoordsets()                                                             # docked = docked_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_coords = prody.parsePDB(input_crystal_path).getCoords()                                                              # crystal = prody_crystal123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                                                        # the reason is to know that this thing is an object123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        expanded_docked = np.expand_dims(docked_coords, -2)                                                                    # 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        diff = expanded_docked - crystal_coords                                                                                # 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        distance = np.sqrt(np.sum(np.power(diff, 2), axis=-1))                                                          # 3 in one line123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                                                        # !!!!!! Formula is not correct                                                                               # sum = min123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        all_clash = (distance < clash_cutoff_A).astype(float)                                                    #1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        atom_clash = (np.sum(all_clash, axis=-1) > 0).astype(float)                                                     #2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        position_clash_ratio = np.mean(atom_clash, axis=-1)                                                             #3 : 1,2,3 in one line123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i, ratio in enumerate(position_clash_ratio):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            records.append(input_data + [i + 1, ratio, 1, 'success'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = input_data + [1, 0, 0, str(e)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)                                                                                       # failure mssg123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef rmsd(table_idx, param, input_data):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor, chain, resnum, resname = input_data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_folder = param['input_docked_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_folder = param['input_crystal_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_name = '_'.join([receptor, chain, resnum, resname, 'ligand']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_dir = os.path.join(data_dir,input_docked_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_path = os.path.join(input_docked_dir, lig_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_dir = os.path.join(data_dir, input_crystal_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_path = os.path.join(input_crystal_dir, lig_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_coords = prody.parsePDB(input_docked_path).getCoordsets()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_coord = prody.parsePDB(input_crystal_path).getCoords()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rmsd = np.sqrt(np.mean(np.sum(np.square(docked_coords - crystal_coord), axis=01), axis=-1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i, rd in enumerate(rmsd):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            records.append(input_data + [i + 1, rd, 1, 'success'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = input_data + [1, 0, 0, str(e)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef native_contact(table_idx, param, input_data):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor, chain, resnum, resname = input_data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_folder = param['input_docked_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_folder = param['input_crystal_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_folder = param['input_receptor_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        distance_threshold = param['distance_threshold']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_name = '_'.join([receptor, chain, resnum, resname, 'ligand']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_name = '_'.join([receptor, chain, resnum, resname, 'receptor']) + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_dir = os.path.join(data_dir, input_docked_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_docked_path = os.path.join(input_docked_dir, lig_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_dir = os.path.join(data_dir, input_crystal_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_crystal_path = os.path.join(input_crystal_dir, lig_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_dir = os.path.join(data_dir, input_rec_folder, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_rec_path = os.path.join(input_rec_dir, rec_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parsed_docked =  prody.parsePDB(input_docked_path).select('not hydrogen')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parsed_crystal = prody.parsePDB(input_crystal_path).select('not hydrogen')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parsed_rec = prody.parsePDB(input_rec_path).select('not hydrogen')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cry_atom_num = parsed_crystal.numAtoms()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_atom_num = parsed_docked.numAtoms()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        assert cry_atom_num == lig_atom_num123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_coords = parsed_docked.getCoordsets()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        crystal_coord = parsed_crystal.getCoords()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_coord = parsed_rec.getCoords()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        exp_crystal_coord = np.expand_dims(crystal_coord, -2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cry_diff = exp_crystal_coord - rec_coord123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cry_distance = np.sqrt(np.sum(np.square(cry_diff), axis=-1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        exp_docked_coords = np.expand_dims(docked_coords, -2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_diff = exp_docked_coords - rec_coord123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        docked_distance = np.sqrt(np.sum(np.square(docked_diff),axis=-1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cry_contact = (cry_distance < distance_threshold).astype(int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        num_contact = np.sum(cry_contact).astype(float)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_contact = (docked_distance < distance_threshold).astype(int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        contact_ratio = np.sum(cry_contact * lig_contact, axis=(-1,-2)) / num_contact123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i , nt in enumerate(contact_ratio):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            records.append(input_data + [i + 1, nt, 1, 'success'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        record = input_data + [0, 0, 0, str(e)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [record]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef binding_affinity(table_idx, param, input_data):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pdb_bind_index = param['pdb_bind_index']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pdb_bind_index = config.binding_affinity_files[pdb_bind_index]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        PDB_bind = read_PDB_bind(pdb_bind_index=pdb_bind_index)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        records = [[PDB_bind.pdb_names[i].upper(), PDB_bind.ligand_names[i],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 PDB_bind.log_affinities[i], PDB_bind.normalized_affinities[i],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 1, 'success']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 for i in range(len(PDB_bind.pdb_names))]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db.insert(table_idx, records)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print (e)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFDatabaseAction={123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'download':download,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'split_ligand':split_ligand,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'split_receptor':split_receptor,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'reorder':reorder,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'smina_dock':smina_dock,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'overlap':overlap,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'rmsd':rmsd,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'native_contact':native_contact,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'binding_affinity':binding_affinity123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}