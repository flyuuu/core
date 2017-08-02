from collections import namedtuple, OrderedDict
table = namedtuple('Table',['type','columns','primary_key'])

tables = {
    'reorder_ligand':table(*['reorder',
                     OrderedDict(
                        [
                            ('receptor','text'),
                            ('chain','text'),
                            ('resnum','text'),
                            ('resname','text'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                     ),
                     ['receptor','chain','resnum','resname']
                ]),
    'docked_ligand':table(*['docked',
                     OrderedDict(
                        [
                            ('receptor','text'),
                            ('chain','text'),
                            ('resnum','text'),
                            ('resname','text'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                     ),
                     ['receptor','chain','resnum','resname']
                ]),

    'overlap':table(*['overlap',
                        OrderedDict(
                            [
                                ('receptor','text'),
                                ('chain','text'),
                                ('resnum','text'),
                                ('resname','text'),
                                ('position','integer'),
                                ('overlap_ratio','real'),
                                ('state','integer'),
                                ('comment','text')
                            ]
                        ),
                        ['receptor','chain','resnum','resname','position']]),
    'rmsd':table(*['rmsd',
                    OrderedDict(
                        [
                            ('receptor','text'),
                            ('chain','text'),
                            ('resnum','text'),
                            ('resname','text'),
                            ('position','integer'),
                            ('rmsd','real'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                    ),
                    ['receptor','chain','resnum','resname','position']]),
    'native_contact':table(*['native_contact',
                    OrderedDict(
                        [
                            ('receptor','text'),
                            ('chain','text'),
                            ('resnum','text'),
                            ('resname','text'),
                            ('position','integer'),
                            ('native_contact','real'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                    ),
                   ['receptor','chain','resnum','resname','position']]),
    'binding_affinity':table(*['binding_affinity',
                    OrderedDict(
                        [
                            ('receptor','text'),
                            ('resname','text'),
                            ('log_affinity','real'),
                            ('norm_affinity','real'),
                            ('state','ingeter'),
                            ('comment','text')
                        ]
                    ),
                    ['receptor','resname']]),
}

