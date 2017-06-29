import openbabel as ob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass mol:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self, file_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Load and prepare ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        file_path:: path of the input pdb123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fPath = file_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.read(file_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.get_bonds()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.get_atom_group()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.get_branch_group()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.get_atom_mask()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.get_atom_coord()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.get_rotate_vector()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def rotate(self, bidx, rot_ang, side):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Rotate ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        bidx:: id for the rotate bond123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rot_ang:: rotation angle123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        side:: 0 or 1 since rotate bond divide ligand into 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        T, T_ = self.get_translation_mat(self.starts[bidx])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rot_mat = self.rotate_on_ori(self.unit_vectors[bidx], rot_ang)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        trans_1 = np.transpose(np.dot(T, np.transpose(self.ext_coords)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        trans_2 = np.transpose(np.dot(rot_mat, np.transpose(trans_1)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        trans_3 = np.transpose(np.dot(T_, np.transpose(trans_2))[:3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        side_mask = (self.rotate_masks[bidx].reshape(-1,1) == side).astype(np.float)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rotated = side_mask * trans_3 + ( 1 - side_mask ) * self.coords 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return rotated123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def read(self, file_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Read pdb file by openbabel123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        file_path:: path of the input pdb123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        obConversion = ob.OBConversion()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.obmol = ob.OBMol()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        read = obConversion.ReadFile(self.obmol, file_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if read == False:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("Cannot read {}".format(file_path))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_bonds(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Find the rotable bonds in ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rot_bond = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        c = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rot_bonds = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        all_bonds = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for bond in ob.OBMolBondIter(self.obmol):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            atom_pair =[bond.GetBeginAtomIdx()-1, bond.GetEndAtomIdx()-1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            atom_pair = tuple(sorted(atom_pair))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            all_bonds.append(atom_pair)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            #print (not bond.IsSingle(), bond.IsAmide(), bond.IsInRing())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            #print (bond.GetBeginAtom().GetValence(), bond.GetEndAtom().GetValence())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if not bond.IsSingle() or bond.IsAmide() or bond.IsInRing():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                c +=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                continue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            elif bond.GetBeginAtom().GetValence() ==1 or bond.GetEndAtom().GetValence() ==1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                c +=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                continue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                rot_bonds.append(atom_pair)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                c +=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                rot_bond += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.rot_bonds = rot_bonds123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.all_bonds = all_bonds123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def dfs_split(self, idx, bidx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Split ligand into different rigid body123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx:: id for the atom linked by the bond123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        bidx:: id for current branch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.branch[idx] = bidx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        bonds = filter(lambda x:x[0]==idx or x[1]==idx, self.all_bonds)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for bond in bonds:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if bond[0]==idx:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                begin = bond[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                end = bond[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                begin = bond[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                end = bond[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if self.branch[end]>=0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    continue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if bond in self.rot_bonds:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    n_bidx = max(self.branch)+1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.branch_bonds.append(tuple(sorted([bidx,n_bidx])))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.branch_rot_bonds.append(bond)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.dfs_split(end, n_bidx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.dfs_split(end, bidx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_atom_group(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Split ligand into different rigid body123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.branch = [-1] * self.obmol.NumAtoms()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.branch_bonds = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.branch_rot_bonds = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.dfs_split(0,0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def label_branch(self, midx, bidx, label, rotbond):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Divide branchs by rotable bonds123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        midx:: id for current rotable bond123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        bidx:: id for current branch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        label:: 0 or 1 since rotable bond divide ligand into 2 parts123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rotbond:: tuple current rotable bond123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.branch_mask[midx][bidx] = label123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        bonds = filter(lambda x:x[0]==bidx or x[1]==bidx, self.branch_bonds)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for bond in bonds:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if bond == rotbond:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                continue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if bond[0] == bidx:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                begin = bond[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                end = bond[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                begin = bond[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                end = bond[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if self.branch_mask[midx][end] >= 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                continue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.branch_mask[midx][end] = label123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.label_branch(midx, end, label, rotbond)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_branch_group(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Divide branchs by rotable bonds123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.branch_mask = np.ones((len(self.rot_bonds), len(set(self.branch)))) * -1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i, bond in enumerate(self.branch_bonds):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.label_branch(i, bond[0], 0, bond)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.label_branch(i, bond[1], 1, bond)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_atom_mask(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Divide atoms group by rotable bonds123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.atom_mask = np.ones((len(self.rot_bonds), self.obmol.NumAtoms())) * -1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i, b_mask in enumerate(self.branch_mask):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for bidx in np.where(self.branch_mask[i]==0)[0]:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.atom_mask[i][np.where(self.branch == bidx)] = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for bidx in np.where(self.branch_mask[i]==1)[0]:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.atom_mask[i][np.where(self.branch == bidx)] = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_atom_coord(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Get coordinate of the atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coords = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for obatom in ob.OBMolAtomIter(self.obmol):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            coords.append([obatom.x(), obatom.y(), obatom.z()])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.coords = np.asarray(coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.ext_coords = np.hstack((coords,np.ones((self.coords.shape[0],1))))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_rotate_vector(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Prepare rotate vector and rotate atom mask for all rotable bonds123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        unit_vectors = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        starts = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rotate_masks =[]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for rbidx, bond in enumerate(self.branch_rot_bonds):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            vector = self.coords[bond[0]] - self.coords[bond[1]]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            unit_vector = vector/ np.sqrt(np.sum(np.square(vector),axis=-1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            start = self.coords[bond[0]]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            mask = self.atom_mask[rbidx]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            unit_vectors.append(unit_vector)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            starts.append(start)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rotate_masks.append(mask)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.unit_vectors = unit_vectors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.starts = starts123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.rotate_masks = rotate_masks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_translation_mat(self, origin):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Prepare matrix shifts between origin point and (0,0,0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        T = np.asarray([123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [1,0,0, -origin[0]],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [0,1,0, -origin[1]],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [0,0,1, -origin[2]],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [0,0,0, 1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        T_ = np.asarray([123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [1,0,0, origin[0]],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [0,1,0, origin[1]],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [0,0,1, origin[2]],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [0,0,0,1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return T, T_123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def rotate_on_ori(self, vec, theta):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Prepare matrix rotate along vec 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cos = np.cos123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sin = np.sin123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        u,v,w = vec[0], vec[1], vec[2]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rotmat = [123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                u**2 + (1-u**2)*cos(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                u*v*(1-cos(theta)) - w*sin(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                u*w*(1-cos(theta)) + v*sin(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                u*v*(1-cos(theta)) + w*sin(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                v**2 + (1-v**2)*cos(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                v*w*(1-cos(theta)) - u*sin(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                u*w*(1-cos(theta)) - v*sin(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                v*w*(1-cos(theta)) + u*sin(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                w**2 + (1-w**2)*cos(theta),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rotmat = np.asarray(rotmat)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return rotmat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # read pdb file 'ligand.pdb'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand = mol('ligand.pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # rotate along first rotable bond, rotation angle is 1 rad, rotate the latter part of the ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotated_coord = ligand.rotate(0, 1, 1)