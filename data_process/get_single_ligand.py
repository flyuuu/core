import numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pandas as pd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport config123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os,sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport shutil123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF'''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFIn our current database docking result of same crystal ligands stored in one file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFThis code use obabel to convert specific ligand from file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFand store them orderly in given path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFThe souce is a csv file contain columns ['PDBname','PDBResId']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF'''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_pdb_and_crystal(input_file):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # source to place crystal ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    crystal_source = os.path.join(config.BASE_DATA, 'H', 'addH')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # dest to place converted ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    crystal_dest = os.path.join(config.BASE_DATA, 'filter_rmsd', 'crystal_ligands')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(crystal_dest):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.mkdir(crystal_dest)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # source to place pdb123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pdb_source = os.path.join(config.BASE_DATA, 'H', 'data')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # dest to place pdb123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pdb_dest = os.path.join(config.BASE_DATA, 'filter_rmsd', 'receptors')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(pdb_dest):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.mkdir(pdb_dest)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #dirname = os.path.dirname(input_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #receptor = os.path.basename(dirname)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor = input_file.split('_')[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename = input_file+'_ligand'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_in = os.path.join(pdb_source,receptor,receptor+'.pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shutil.copy(receptor_in,pdb_dest)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    crystal_in = os.path.join(crystal_source,receptor,filename+'.pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    crystal_path = os.path.join(crystal_dest,receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(crystal_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.mkdir(crystal_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    crystal_out = os.path.join(crystal_path,filename+'.pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(crystal_out):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cmd = 'obabel -ipdb %s -opdb -O %s -d'%(crystal_in,crystal_out)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.system(cmd)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef convert(item):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    PDB =item['PDBname']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    RS = item['PDBResId']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    RES,Id = RS.split('_')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    source_base = '/n/scratch2/xl198/data/result'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    source_file_path= os.path.join(source_base,PDB,'_'.join([PDB,RES,'ligand','fast.mol']))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dest_base = '/n/scratch2/xl198/data/filter_rmsd/docked_ligands'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(dest_base):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.mkdir(dest_base)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dest_path = os.path.join(dest_base,PDB)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not os.path.exists(dest_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.mkdir(dest_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dest_file_path = os.path.join(dest_path,'_'.join([PDB,RES,'ligand','fast',Id+'.pdb']))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cmd = 'obabel -imol2 %s -f %s -l %s -opdb -O %s '%(source_file_path,Id,Id,dest_file_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    os.system(cmd)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef run(base, offset):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    df = pd.read_csv('/home/xl198/remark/dec_1.csv')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    convert(df.ix[base*1000+offset-1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    get_pdb_and_crystal(df.ix[base*1000+offset-1]['ID'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    get crystal ligand and receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    df = pd.read_csv('/n/scratch2/xl198/data/remark/valid.csv')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i in range(len(df)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        get_pdb_and_crystal(df.ix[i]['ID'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    args = sys.argv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if len(args) >= 3:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        base = int(args[1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        offset = int(args[2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print 'base %d offset %d' % (base, offset)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        run(base, offset)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    main()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF