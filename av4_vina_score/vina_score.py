import os, sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom eval import evaluation123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom option import get_parser123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef test():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    v = evaluation(FLAGS.receptor, FLAGS.ligand, FLAGS.debug, FLAGS.log)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    v.eval()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef landscape():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    v = evaluation(FLAGS.receptor, FLAGS.ligand, FLAGS.debug, FLAGS.log)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    shift_coords = [[x, y, z] for x in np.linspace(-1, 1, 21) for y in np.linspace(-1, 1, 21) for z in123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    np.linspace(-1, 1, 21)]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    landscape = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for shift in shift_coords:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        v.set_transform(shift=shift)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        e = v.eval()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        landscape.append(shift + [e])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    np.save('energy_map.npy', np.asarray(landscape))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    landscape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #test()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser = get_parser()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS, unparsed = parser.parse_known_args()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    main()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF