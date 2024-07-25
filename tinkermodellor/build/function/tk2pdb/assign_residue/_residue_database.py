from typing import List, Tuple, Dict

class GraphData():
    # Define Node and Edge data types
    Node = Tuple[int, Dict[str, str]]  # Node type: (Node ID, attribute dictionary)
    Edge = Tuple[int, int]  # Edge type: (Start Node ID, End Node ID, attribute dictionary)
    Resname: str 
    AtonNum: int

class ResidueDatabase():
    
    # Format:          [Node Data, Edge Data, Residue Name, Number of Atoms]
    database: List[GraphData] = []
    
    database = [
        #Residue TRP
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'N'}),
                (9, {'element': 'C'}),
                (10, {'element': 'C'}),
                (11, {'element': 'C'}),
                (12, {'element': 'C'}),
                (13, {'element': 'C'}),
                (14, {'element': 'C'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (8, 9,),
                (9, 10,),
                (6, 10,),
                (10,11,),
                (11,12,),
                (12,13,),
                (13,14,),
                (14, 9,),
            ],
            'TRP',
            14
        ],
        #Residue TYR
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'C'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'O'}),
                (9, {'element': 'C'}),
                (10, {'element': 'C'}),
                (11, {'element': 'C'}),
                (12, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (4, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (7, 9,),
                (9,10,),
                (10,4,),
                (2,11,),
                (11,12,),
            ],
            'TYR',
            12
        ],
        #Residue PHE
        [
           [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'C'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'C'}),
                (9, {'element': 'C'}),
                (10,{'element': 'C'}),
                (11,{'element': 'O'}),
           ],
           [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (4, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (8, 9,),
                (9, 4,),
                (10,2,),
                (11,10,),
           ],
           'PHE',
           11
        ],
        #Residue ARG 
        [
            [   (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'C'}),
                (5, {'element': 'C'}),
                (6, {'element': 'N'}),
                (7, {'element': 'C'}),
                (8, {'element': 'N'}),
                (9, {'element': 'N'}),
                (10, {'element': 'C'}),
                (11, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (4, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (7, 9,),
                (2,10,),
                (10,11,),
            ],
            'ARG',
            11
        ],

        #Residue HISD 
        [
            [   (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'N'}),
                (8, {'element': 'C'}),
                (9, {'element': 'N'}),
                (10,{'element': 'C'}),
                (11,{'element': 'H'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (8, 9,),
                (9,10,),
                (10,6,),
                (11,7,),
            ],
            'HIS',
            10
        ],

        #Residue HISE 
        [
            [   (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'N'}),
                (8, {'element': 'C'}),
                (9, {'element': 'N'}),
                (10,{'element': 'C'}),
                (11,{'element': 'H'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (8, 9,),
                (9,10,),
                (10,6,),
                (11,9,),
            ],
            'HIS',
            10
        ],

        #Residue HISH, two hydrogen atoms are attached to the nitrogen atom 
        [
            [   (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'N'}), # ND
                (8, {'element': 'C'}),
                (9, {'element': 'N'}), # NE
                (10,{'element': 'C'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (8, 9,),
                (9,10,),
                (10,6,),
            ],
            'HISh',
            10
        ],
        #Residue GLUH
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'O'}),
                (9, {'element': 'O'}),
                (10, {'element': 'H'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (7, 9,),
                (9, 10,),
            ],
            'GLUH',
            9
        ],

        #Residue GLU
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'O'}),
                (9, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (7, 9,),
            ],
            'GLU',
            9
        ],

        #Residue LYS
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'C'}),
                (9, {'element': 'N'}),
                (10, {'element': 'H'}),
                (11, {'element': 'H'}),
                (12, {'element': 'H'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (8, 9,),
                (9, 10,),
                (9, 11,),
                (9, 12,),
            ],
            'LYS',
            9
        ],

        #Residue LYSN, deprotonated lysine
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'C'}),
                (9, {'element': 'N'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (8, 9,),
            ],
            'LYSN',
            9
        ],
        #Residue GLN
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'O'}),
                (9, {'element': 'N'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,),
                (7, 9,),
            ],
            'GLN',
            9
        ],
        #Residue ASPH
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'C'}),
                (5, {'element': 'O'}),
                (6, {'element': 'O'}),
                (7, {'element': 'H'}),
                (8, {'element': 'C'}),
                (9, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (4, 5,),
                (4, 6,),
                (6, 7,),
                (2, 8,),
                (8, 9,),
            ],
            'ASPH',
            8
        ],
        #Residue ASP
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'C'}),
                (5, {'element': 'O'}),
                (6, {'element': 'O'}),
                (7, {'element': 'C'}),
                (8, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (4, 5,),
                (4, 6,),
                (2, 7,),
                (7, 8,),
            ],
            'ASP',
            8
        ],
        #Residue LEU
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'C'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (6, 8,),
            ],
            'LEU',
            8
        ],
        #Residue ILE
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'C'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (5, 8,),
            ],
            'ILE',
            8
        ],

       #Residue MET
       [
           [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'S'}),
                (8, {'element': 'C'}),
           ],
           [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 8,), 
           ],
           'MET',
           8
       ],
        #Residue ASN
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'O'}),
                (8, {'element': 'N'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (6, 8,),
            ],
            'ASN',
            8
        ],
        #Residue THR
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (5, 7,), 
            ],
        'THR',
        7
        ],
        #Residue PRO
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (7, 1,),
            ],
            'PRO',
            7
        ],
        #Residue VAL
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'C'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (3, 5,),
                (2, 6,),
                (6, 7,),
            ],
            'VAL',
            7
        ],
        #Residue CYX
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'S'}),
                (7, {'element': 'H'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
            ],
            'CYX',
            6
        ],
        #Residue CYS
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'S'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
            ],
            'CYS',
            6
        ],
        #Residue SER
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'O'}), 
            ],
            [
                
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
            ],
            'SER',
            6
        ],   
        
        #Resideu ALA
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'H'}),
                (5, {'element': 'H'}),
                (6, {'element': 'H'}),
                (7, {'element': 'C'}),
                (8, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (4, 3,),
                (5, 3,),
                (6, 3,),
                (2, 7,),
                (7, 8,),
            ],
            'ALA',
            5
        ],

        # Residue GLY
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'H'}),
                (4, {'element': 'H'}),
                (5, {'element': 'C'}),
                (6, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (2, 4,),
                (2, 5,),
                (6, 5,),
            ],
            'GLY',
            4
        ],
        # Water
        [
            [
                (1, {'element': 'O'}),
                (2, {'element': 'H'}),
                (3, {'element': 'H'}),
            ],
            [
                (1, 2,),
                (1, 3,),
            ],
            'H2O',
            3
        ],
    ]
