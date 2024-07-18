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
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'C'}),
                (9, {'element': 'C'}),
                (10, {'element': 'O'}),
                (11, {'element': 'C'}),
                (12, {'element': 'O'}),
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
                (10,11,),
                (6,11,),
                (9,12,),
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
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'S'}),
                (8, {'element': 'C'}),
                (9, {'element': 'N'}),
                (10,{'element': 'C'}),
                (11,{'element': 'C'}),
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
                (10,11,),
                (11, 6,),
           ],
           'PHE',
           11
        ],
        #Residue ARG 
        [
            [   (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'N'}),
                (9, {'element': 'C'}),
                (10, {'element': 'N'}),
                (11, {'element': 'N'}),
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
                (10,11,),
            ],
            'ARG',
            11
        ],

        #Residue HIS 
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
            'HIS',
            10
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
            'LYS',
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

        #Residue ASP
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'O'}),
                (8, {'element': 'O'}),
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
        #Resideu VAL
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'elemnnt': 'C'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (5, 7,),
            ],
            'VAL',
            7
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
        
        #Resideu AlA
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
            ],
            'ALA',
            5
        ],

        # Residue GLY
        [
            [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
            ],
            [
                (1, 2,),
                (2, 3,),
                (3, 4,),
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
