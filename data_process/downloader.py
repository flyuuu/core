import os, sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport prody123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport getopt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pandas as pd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy  as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport multiprocessing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport threading123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass parseRCSB:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Download pdb from rcsb and split it into receptor and ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #2 what is rcsb - how does it work aka 1,2,3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.get_address = lambda PDB: 'https://files.rcsb.org/download/' + PDB + '.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.thread_num = FLAGS.thread_num123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.process_num = FLAGS.process_num123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.log_file = FLAGS.log_file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.get_dataframe()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_dataframe(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        content = open('target_PDB.txt').readline()                     #1 content of what and where123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        content = content.split(',')                                    # I assume you are reading pdbs from the text file ?123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        content = map(lambda x: x.strip(), content)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pdb_list = content123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def error_log(self, content):                                       #3 again "content" ?123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # write down error information123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        with open(self.log_file, 'a') as fout:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            fout.write(content)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def downloads(self, item):                                          #4 name of the function is not informative123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Download pdb from rcsb and split it into receptor and ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :param item: 4 letter PDB ID '3EML'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Download pdb to rowdata_folder123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        download_address = self.get_address(item)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        os.system('wget -P {} {}'.format(FLAGS.rowdata_folder,download_address))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # create folder to store ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pdbname = item.lower()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_folder = os.path.join(FLAGS.splited_ligand_folder, pdbname)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not os.path.exists(ligand_folder):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.mkdir(ligand_folder)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # parse pdb123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            parsed = prody.parsePDB(os.path.join(FLAGS.rowdata_folder, item + '.pdb'))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        except:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.error_log('can not parse {}.\n'.format(item))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # select receptor and ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        hetero = parsed.select('(hetero and not water) or resname ATP or resname ADP')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor = parsed.select('protein or nucleic')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if receptor is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.error_log("{} doesn't have receptor.\n".format(item))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if hetero is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.error_log("{} doesn't have ligand.\n".format(item))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #5 I would create a printable class "statistics"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_flags = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for each in prody.HierView(hetero).iterResidues():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if each.numAtoms() <= FLAGS.atom_num_threahold:                                     # 6there will be many thresholds123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                                # let's organize them together into a class FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                # ignore ligand if atom num is less than threshold123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                continue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                ligand_flags = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                ResId = each.getResindex()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                ligand_path = os.path.join(FLAGS.splited_ligand_folder, pdbname,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                           "{}_{}_ligand.pdb".format(pdbname, ResId))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if not os.path.exists(os.path.dirname(ligand_path)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    os.mkdir(os.path.dirname(ligand_path))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                prody.writePDB(ligand_path, each)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if ligand_flags:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            receptor_path = os.path.join(FLAGS.splited_receptor_folder, pdbname + '.pdb')               # 7 splited receptor folder is a bad name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            prody.writePDB(receptor_path, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.error_log("{} doesn't convert, no ligand have more than 10 atoms.\n")                  #8 look at #5 single class "statistics" would help123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def thread_convert(self, func, dataframe, index):                                                   #9 what does "thread convert mean" ????123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i in index:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            func(dataframe[i])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def process_convert(self, func, dataframe, index):                                                  #10 what does "process convert mean" ???123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # linspace contain end value but range don't123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # so we use edge[i+1] to select value in index123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # end should be len(index)-1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if len(index) < self.thread_num:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for i in index:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                func(dataframe[i])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        edge = np.linspace(0, len(index) - 1, self.thread_num + 1).astype(int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        thread_list = [threading.Thread(target=self.thread_convert,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                        args=(func,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                              dataframe,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                              range(index[edge[i]],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                    index[edge[i + 1]])))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       for i in range(self.thread_num)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for t in thread_list:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            t.start()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for t in thread_list:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            t.join()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def convert(self):                                                                                  #11 we already have "thread convert","process convert"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        convert_func = self.downloads                                                                   # convert is a bad name now123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # when there's not enough entry to comvert , decrease thread's num123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if len(self.pdb_list) < self.process_num * self.thread_num:                                     #12 not necessary function that takes space- comment it out123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for i in range(len(self.pdb_list)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                convert_func(self.pdb_list[i])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        edge = np.linspace(0, len(self.pdb_list), self.process_num + 1).astype(int)                     #13 what does "edge" mean123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        process_list = [multiprocessing.Process(target=self.process_convert,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                args=(convert_func,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                      self.pdb_list,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                      range(edge[i],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                            edge[i + 1])))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        for i in range(self.process_num)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for p in process_list:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "process start: ", p123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            p.start()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for p in process_list:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "process end: ", p123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            p.join()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass FLAGS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    workplace = '/n/scratch2/xl198/data/rcsb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rowdata_folder = os.path.join(workplace, 'row')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    splited_receptor_folder = os.path.join(workplace, 'row_receptor')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    splited_ligand_folder = os.path.join(workplace, 'ligands')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    log_file = 'error.log'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    thread_num = 16123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    process_num = 12123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    atom_num_threahold = 10123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser = parseRCSB()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.convert()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#14 downloader.py is not informative at all