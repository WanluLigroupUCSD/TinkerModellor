from typing import List, Tuple, Dict

class GraphData():
    # Define Node and Edge data types
    Node = Tuple[int, Dict[str, str]]  # Node type: (Node ID, attribute dictionary)
    Edge = Tuple[int, int, Dict[str, str]]  # Edge type: (Start Node ID, End Node ID, attribute dictionary)

class ResidueDatabase():
    
    # Format: [Node Data, Edge Data, Residue Name, Number of Atoms]
    
    database = [
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

    ]
    