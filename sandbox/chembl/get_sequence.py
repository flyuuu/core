import os, sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport prody123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tempfile123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#import chembl123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport subprocess123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport xml.dom.minidom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom chembl_blast import chembl_blast123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef parse_PDB(PDBname):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	Parse the structure from Protein Data Bank123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	args: 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		PDBname :: str123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		4 letters identifier for the strcuture123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	cdir = os.getcwd()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	tdir = tempfile.mkdtemp()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	os.chdir(tdir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	PDBHead = prody.parsePDBHeader(PDBname)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	PDB = prody.parsePDB(PDBname)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	ligands = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	for chem in PDBHead['chemicals']:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ligands.append([chem.chain, str(chem.resnum), chem.resname, chem.name])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	for chain, resnum, resname, name in ligands:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    	# select the receptor and the ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		receptor = PDB.select('not (chain {} resnum {})'.format(chain, resnum))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		ligand = PDB.select('chain {} resnum {}'.format(chain, resnum))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		cen_ligand = prody.calcCenter(ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		around_atoms = receptor.select('within 20 of center', center=cen_ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		hv = around_atoms.getHierView()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		sequence = hv['A'].getSequence()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		blast = chembl_blast(sequence)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		result = (PDBname, [chain, resnum, resname], blast)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF		yield result123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    p = parse_PDB("3eml")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF