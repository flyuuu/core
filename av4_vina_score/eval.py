import os, sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom openbabel import OBAtom, OBElementTable123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport openbabel123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom atom_parse import Atom_dict123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom atom_parse import atom_parser as Atom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom collections import namedtuple123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom functools import partial123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass evaluation:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    const_v = 1000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    const_cap = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    const_cutoff = 8123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    const_smooth = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    const_epsilon = 2.22045e-16123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self, receptor, ligand, debug, log):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # parse receptor and ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.obabel_load(receptor, ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # create scoring function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.create_scoring_functions()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # set transform parameter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.set_transform()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.debug = debug123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.log = log123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def debug_info(self, message):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if self.debug == 'print':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print message123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        elif self.debug == 'log':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            with open(self.log, 'a') as fout:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                fout.write(message + '\n')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        elif self.debug == 'off':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def obabel_load(self, receptor, ligand):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        load ligand and receptor through openbabel123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        obConversion = openbabel.OBConversion()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OBligand = openbabel.OBMol()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.debug_info('Parse {} by openbabel.'.format(ligand))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not obConversion.ReadFile(OBligand, ligand):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            message = 'Cannot parse {}'.format(ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception(message)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OBligand.DeleteNonPolarHydrogens()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OBligand.AddPolarHydrogens()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # lig_atoms = [obatom for obatom in openbabel.OBMolAtomIter(OBligand)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.lig = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for obatom in openbabel.OBMolAtomIter(OBligand):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            atom = Atom(obatom)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.lig.append(atom)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OBreceptor = openbabel.OBMol()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.debug_info('Parse {} by opnbabel.'.format(receptor))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not obConversion.ReadFile(OBreceptor, receptor):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            message = 'Cannot parse {}.'.format(receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception(message)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OBreceptor.DeleteNonPolarHydrogens()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OBreceptor.AddPolarHydrogens()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # rec_atoms = [obatom for obatom in openbabel.OBMolAtomIter(OBreceptor)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.rec = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for obatom in openbabel.OBMolAtomIter(OBreceptor):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            atom = Atom(obatom)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.rec.append(atom)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def opt_distance(self, atom_a, atom_b):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return atom_a.get_atom().xs_radius + atom_b.get_atom().xs_radius123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def curl(self, e):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if e > 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tmp = 1.0 * self.const_v / (self.const_v + e)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            e *= tmp123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def not_hydrogen(self, atom):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return not atom.smina_name.endswith('Hydrogen')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def h_bond_possible(self, atom_a, atom_b):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return (atom_a.get_atom().xs_donor and atom_b.get_atom().xs_acceptor) or (123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            atom_a.get_atom().xs_acceptor and atom_b.get_atom().xs_donor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def anti_h_bond(self, atom_a, atom_b):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if (atom_a.get_atom().xs_donor and not atom_a.get_atom().xs_acceptor):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return atom_b.get_atom().xs_donor and not atom_b.get_atom().xs_acceptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if (not atom_a.get_atom().xs_donor and atom_a.get_atom().xs_acceptor):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return not atom_b.get_atom().xs_doner and atom_b.get_atom().xs_acceptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def slope_step(self, surface_distance, bad, good):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if bad < good:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if surface_distance <= bad:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if surface_distance >= good:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if surface_distance >= bad:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if surface_distance <= good:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return 1.0 * (surface_distance - bad) / (good - bad)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def guass(self, atom_a, atom_b, distance, o=3., w=2.):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        opt_distance = self.opt_distance(atom_a, atom_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        surface_distance = distance - opt_distance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        e = np.exp(-np.power((surface_distance - o) / w, 2))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def vdw(self, atom_a, atom_b, distance, m=12, n=6):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        opt_distance = self.opt_distance(atom_a, atom_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        c_i = np.power(opt_distance, n) * m / (n - m)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        c_j = np.power(opt_distance, m) * n / (m - n)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if distance > opt_distance + self.const_smooth:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            distance -= self.const_smooth123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        elif distance < opt_distance - self.const_smooth:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            distance += self.const_smooth123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            distance = opt_distance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        r_i = np.power(distance, n)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        r_j = np.power(distance, m)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if (r_i > self.const_epsilon or r_j > self.const_epsilon):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return min(self.const_cap, c_i / r_i + c_j / r_j)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return self.const_cap123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def non_dir_h_bond_lj(self, atom_a, atom_b, distance, offset):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if self.h_bond_possible(atom_a, atom_b):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            d0 = offset + self.opt_distance(atom_a, atom_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            n = 10123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            m = 12123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            depth = 5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            c_i = np.power(d0, n) * depth * m / (n - m)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            c_j = np.power(d0, m) * depth * n / (m - n)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            r_i = np.power(distance, n)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            r_j = np.power(distance, m)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if (r_i > self.const_epsilon or r_j > self.const_epsilon):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return min(self.const_cap, c_i / r_i + c_j / r_j)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return self.const_cap123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def replusion(self, atom_a, atom_b, distance, offset=0.):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        diff = distance - offset - self.opt_distance(atom_a, atom_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return np.power(diff, 2) if diff < 0 else 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def hydrophobic(self, atom_a, atom_b, distance, good, bad):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if atom_a.get_atom().xs_hydrophobe and atom_b.get_atom().xs_hydrophobe:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            surface_distance = distance - self.opt_distance(atom_a, atom_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return self.slope_step(surface_distance, bad=bad, good=good)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def non_hydrophobic(self, atom_a, atom_b, distance, good, bad):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not atom_a.get_atom().xs_hydrophobe and not atom_b.get_atom().xs_hydrophobe:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            surface_distance = distance - self.opt_distance(atom_a, atom_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return self.slope_step(surface_distance, bad=bad, good=good)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def non_dir_h_bond(self, atom_a, atom_b, distance, good, bad):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if self.h_bond_possible(atom_a, atom_b):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            surface_distance = distance - self.opt_distance(atom_a, atom_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return slope_step(surface_distance, bad=bad, good=good)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def non_dir_anti_h_bond_quadratic(self, atom_a, atom_b, distance, offset):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if self.anti_h_bond(atom_a, atom_b):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            surface_distance = distance - offset - self.opt_distance(atom_a, atom_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if surface_distance > 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return surface_distance * surface_distance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def eval(self, atom_a, atom_b, distance):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        e = self.vdw(atom_a, atom_b, distance)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def eval_intra(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        We assume ligand is rigid, so intra molecular energy doesn't change we .123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Don't need to calculate it yet.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        distance = lambda i, j: np.sqrt(np.sum(np.power(self.lig[i].coords - self.lig[j].coords, 2)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        intra_pairs = [(i, j) for i in range(len(self.lig) - 1) for j in range(i + 1, len(self.lig))]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        eval_pairs = [(self.lig[i], self.lig[j], distance(i, j)) for (i, j) in intra_pairs if123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                      distance(i, j) < self.const_cutoff]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        energy = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for scoring_term in self.scoring_functions:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.debug_info("calculating {} ...".format(scoring_term.name))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            this_e = np.sum(map(lambda (a, b, d): scoring_term.func(a, b, d), eval_pairs))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.debug_info("{} original value {}.".format(scoring_term.name, this_e))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            weighted_energy = scoring_term.weight * this_e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            energy += self.curl(weighted_energy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def eval_inter(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        eval the intermolecular energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return: energy: float weighted score123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        distance = lambda i, j: np.sqrt(np.sum(np.power(self.transform(self.lig[i].coords) - self.rec[j].coords, 2)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # doesn't count hydrogen in receptor and lignad123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        inter_pairs = [(i, j) for i in range(len(self.lig)) for j in range(len(self.rec)) if123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       self.not_hydrogen(self.lig[i].get_atom()) and self.not_hydrogen(self.rec[j].get_atom())]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # filter atom pair which is too far away123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        eval_pairs = [(self.lig[i], self.rec[j], distance(i, j)) for (i, j) in inter_pairs if123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                      distance(i, j) < self.const_cutoff]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        energy = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for scoring_term in self.scoring_function:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.debug_info("calculating {} ...".format(scoring_term.name))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            this_e = np.sum(map(lambda (a, b, d): scoring_term.func(a, b, d), eval_pairs))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.debug_info("{} original value {}.".format(scoring_term.name, this_e))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            weighted_energy = scoring_term.weight * this_e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            energy += self.curl(weighted_energy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def set_transform(self, shift=[0, 0, 0], rotate=[0, 0, 0]):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.shift = shift123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.rotate = rotate123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def transform(self, coords):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # only simple shift now123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return self.shift + coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def eval(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF         We just eval intermolecular energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        e = self.eval_inter()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.debug_info('intermolecular energy {}'.format(e))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def create_scoring_functions(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Combine different scoring terms as final scoring function and assign different weight to each of them.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        scoring_term = namedtuple('scoring_term', ['name', 'weight', 'func'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scoring_function = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scoring_function.append(scoring_term('vdw_12_6', 1.0, partial(self.vdw, m=12, n=6)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scoring_function.append(scoring_term('guass_3_2', 1.0, partial(self.guass, o=3., w=2.)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scoring_function.append(scoring_term('replusion_0', 1.0, partial(self.replusion, offset=0.)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scoring_function.append(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            scoring_term('hydrophobic_0.5_1.5', 1.0, partial(self.hydrophobic, good=0.5, bad=1.5)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scoring_function.append(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            scoring_term('non_dir_h_bond_-0.7_0', 1.0, partial(self.non_dir_h_bond, good=-0.7, bad=0)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scoring_function.append(scoring_term('non_dir_anti_h_bond_quadratic_1', 1.0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                  partial(self.non_dir_anti_h_bond_quadratic, offset=1.)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.scoring_function.append(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            scoring_term('non_dir_h_bond_lj_-1', 1.0, partial(self.non_dir_h_bond_lj, offset=-1.)))