import networkx as nx
from networkx.algorithms import isomorphism

from ._residue_database import GraphData
from ._residue_database import ResidueDatabase

class AssignResidue():

    
    def __init__(self) -> None:
        pass


    def __call__(self, nodes: GraphData.Node, edges: GraphData.Edge, resid: int, resiatoms: int) -> str:
        """
        This function assigns a residue name to a residue based on the residue database.
        Args:
            nodes (GraphData.Node): The nodes of the residue.
            edges (GraphData.Edge): The edges of the residue.
            resid (int): The residue ID.
            resiatoms (int): The number of atoms in the residue.
        Returns:
            str: The residue name.
        """
        
        residue_name = "UKN"  # Unknown, default value if no match is found
        
        # Define Matching Function
        def node_match(n1, n2):
            return n1['element'] == n2['element']
        
        # Create Graph
        G_main = nx.Graph()
        G_main.add_nodes_from(nodes)
        G_main.add_edges_from(edges)
        
        for residue_data in ResidueDatabase.database:
            
            # The number of atoms in the residue (main graph) should be greater than 
            # the number of atoms in the residue database (subgraph)
            if residue_data[3] > resiatoms:
                pass
            else:
                G_sub = nx.Graph()
                G_sub.add_nodes_from(residue_data[0])
                G_sub.add_edges_from(residue_data[1])

                # Matching
                GM = isomorphism.GraphMatcher(G_main, G_sub, node_match=node_match)
                is_subgraph_isomorphic = GM.subgraph_is_isomorphic()
                
                if is_subgraph_isomorphic:
                    residue_name = residue_data[2]
                    break
        
        if residue_name == "UKN":
            
            Warning('Residue ID: {} is not found in the residue database. Assigning residue name as "UKN"'.format(resid))

        return residue_name