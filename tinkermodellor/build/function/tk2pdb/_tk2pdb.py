from typing import List
import numpy as np

from .assign_residue._assign_reside import AssignResidue
from .assign_residue._residue_database import GraphData
from ...system.tinker._tinkersystem import TinkerSystem
#from tinkermodellor.build.function.tk2pdb.assign_residue._assign_reside import AssignResidue
#from tinkermodellor.build.function.tk2pdb.assign_residue._residue_database import GraphData

class Tinker2PDB(TinkerSystem):
    def __init__(self) -> None:
        super().__init__()

        #Used for store the residue name
        self.ResidueName: List[str] = []
        #Used for store the residue number
        self.ResidueNum: np.array = []

    def __call__(self,tk:str, pdb:str) -> None:

        self.read_from_tinker(tk)

        self.ResidueName = ['UNK']*self.AtomNums
        self.ResidueNum = np.zeros(self.AtomNums)

        segment_list = self._split_segement()
        segment_type = self._determine_segment_type(segment_list)
        
        current_residue_index = 1


        for type, index in zip(segment_type, segment_list):
            if type == 'ION':
                self.ResidueName[index[0]:index[-1]] = 'ION'
                self.ResidueNum[index[0]:index[-1]] = current_residue_index
                current_residue_index += 1
            elif type == 'WAT':
                self.ResidueName[index[0]:index[-1]] = 'WAT'
                self.ResidueNum[index[0]:index[-1]] = current_residue_index
                current_residue_index += 1
            else:
                self._assign_residue(index, current_residue_index)

        if pdb != None:
            self.write(pdb)

    def __str__(self) -> str:
        contents = []

        # atoms
        for i in range(self.AtomNums):

            # Format the string for each atom including its index, type, coordinates, and type number.
            # Ensure that the atom type number is aligned correctly without decimal points for integers.
            contents.append(
                "ATOM    "
                f"{(i + 1):5d}  {self.AtomTypesStr[i]:<6}"
                f"{self.ResidueName[i]:>3} "
                f"{self.ResidueNum[i]:>4}    "
                f"{self.AtomCrds[i, 0]:12.6f} "
                f"{self.AtomCrds[i, 1]:12.6f} "
                f"{self.AtomCrds[i, 2]:12.6f} "
                "  1.00  0.00"
            )

            # Append the indices of atoms bonded to the current atom, formatted with appropriate spacing.
            for connect in self.Bonds[i]:
                contents[-1] += f"{connect:6d}"

        return "\n".join(contents)

    def write(self, file_path):
        with open(file_path, 'w') as f:
            f.write(self.__str__())

        
    def _assign_residue(self, index:List[int], residue_index: int) -> str:
        
        find_residue = AssignResidue()
        node : List[GraphData.Node] = []
        edge : List[GraphData.Edge] = []

        last_residue = index[0]

        element = {
            'H': 1,
            'C': 6,
            'N': 7,
            'O': 8,
            'S': 16,
        }

        for i in index:
            # If the atom is C-O-N, then O is the last atom in the residue
            # This is probably a peptide bond
            if self.AtomTypesStr[i-1] == 'N':
                if self.AtomTypesStr[i-3] == 'C' and self.AtomTypesStr[i-2] == 'O':
                    edge = self._clean_edges(edge, 1, i-last_residue)

                    resname = find_residue(node, edge, residue_index, i-last_residue)

                    # last_residue is the index of the first atom in the residue
                    # But ResidueName and ResidueNum are 0-indexed
                    self.ResidueName[last_residue-1:i-2] = resname
                    self.ResidueNum[last_residue-1:i-2] = residue_index
                    
                    residue_index += 1

                    # Update the index of the first atom in the residue
                    last_residue = i
                    
                    # Clear the node and edge
                    node = []
                    edge = []

                    # First atom is always N
                    node.append((i-last_residue+1, {'element': 'N'}))

            # If the atom is CTe-OTe-OTe, then the last OTe is the last atom in the residue
            if self.AtomTypesStr[i-1] == 'OTe':
                if self.AtomTypesStr[i-3] == 'CTe' and self.AtomTypesStr[i-2] == 'OTe':

                    # Diffenet from the peptide bond, the last OTe is the last atom in the residue
                    # But the former process is to find the first atom in the residue (N)
                    # So i should plus 1
                    i+=1

                    edge = self._clean_edges(edge, 1, i-last_residue)

                    resname = find_residue(node, edge, residue_index, i-last_residue)

                    # last_residue is the index of the first atom in the residue
                    # But ResidueName and ResidueNum are 0-indexed
                    self.ResidueName[last_residue-1:i-2] = resname
                    self.ResidueNum[last_residue-1:i-2] = residue_index
                    
                    residue_index += 1

                    # Update the index of the first atom in the residue
                    last_residue = i
                    
                    # Clear the node and edge
                    node = []
                    edge = []

                    # First atom is always N， but this this for next residue in next chain
                    node.append((i-last_residue+1, {'element': 'N'}))

                else:
                    # When meet the first OTe, execute normal process
                    node.append((i-last_residue+1, {'element': f'{self.AtomTypesStr[i-1][0]}'}))

                    for j in self.Bonds[i-1]:
                        if j < i:
                            edge.append((i-last_residue+1, j-last_residue+1))
            
            # Normal process
            else:
                node.append((i-last_residue+1, {'element': f'{self.AtomTypesStr[i-1][0]}'}))

                for j in self.Bonds[i-1]:
                    if j < i:
                        edge.append((i-last_residue+1, j-last_residue+1))
        
        self.AtomTypesStr = []

    def _clean_edges(self, edges:List[GraphData.Edge] , start:int , end: int) -> List[GraphData.Edge]:
        # Remove the bonds, which are not in the residue

        new_edges : List[GraphData.Edge] = []

        for edge in edges:
            for atom_i, atom_2 in edge:
                if atom_i >= start and atom_i <= end and atom_2 >= start and atom_2 <= end:
                    new_edges.append(edge)
    
        return new_edges


    def _split_segement(self):
        
        segment_list = []
        atom_index = 1

        while atom_index <= self.AtomNum:
            residule_list = self._connectivity_search(self, atom_index)
            segment_list.append([residule_list[0], residule_list[-1]])
            atom_index = residule_list[-1]+1
        return segment_list
    
    def _determine_segment_type(segment_list:List[List[int]]) -> List[str]:
        segment_type = []
        for segment in segment_list:
            if len(segment) == 1:
                segment_type.append('ION')
            elif len(segment) == 3:
                segment_type.append('WAT')
            else:
                segment_type.append('BIO')
        return segment_type


    def _connectivity_search(self, initial: int) -> List[int]:
        """
        Finds all atoms connected to the initial atom index, ensuring entire molecules or connected components are marked.

        Args:
            initial (int): Initial atom index to start the search.

        Returns:
            List[int]: Complete list of connected atom indices, sorted.
        """

        residue_list = []
        visited = set()  # Track visited atoms to prevent infinite recursion

        def explore_bonded_atoms(atom_index):
            """Recursively adds bonded atoms to the list."""
            if atom_index in visited:
                return
            visited.add(atom_index)
            residue_list.append(atom_index)

            for bonded_atom in self.Bonds[atom_index - 1]:  # Adjust for 0-indexing
                explore_bonded_atoms(bonded_atom)

        explore_bonded_atoms(initial)

        # Convert sets to sorted lists before returning
        return sorted(residue_list)


if __name__ == '__main__':
        
        find = Tinker2PDB()

        node : GraphData.Node = [
                (1, {'element': 'N'}),
                (2, {'element': 'C'}),
                (3, {'element': 'C'}),
                (4, {'element': 'O'}),
                (5, {'element': 'C'}),
                (6, {'element': 'C'}),
                (7, {'element': 'C'}),
                (8, {'element': 'C'}),
            ]
        edge : GraphData.Edge =[
                (1, 2,),
                (2, 3,),
                (3, 4,),
                (2, 5,),
                (5, 6,),
                (6, 7,),
                (6, 8,),
            ]
        
        atom_number = 8

        resname = find(node, edge, 1, atom_number)
        print(resname)
        
