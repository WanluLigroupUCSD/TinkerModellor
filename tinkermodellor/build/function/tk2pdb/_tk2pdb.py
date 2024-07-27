from typing import List
import sys
import numpy as np

#from tinkermodellor.build.function.tk2pdb.assign_residue._assign_reside import AssignResidue
#from tinkermodellor.build.function.tk2pdb.assign_residue._residue_database import GraphData
#from tinkermodellor.build.system.tinker._tinkersystem import TinkerSystem


from .assign_residue._assign_reside import AssignResidue
from .assign_residue._residue_database import GraphData
from ...system.tinker._tinkersystem import TinkerSystem

class Tinker2PDB(TinkerSystem):
    def __init__(self, depth:int) -> None:
        super().__init__()

        #Used for store the residue name
        self.ResidueName: List[str] = []
        #Used for store the residue number
        self.ResidueNum: np.array = []
        #Used for store the atom type string in pdb
        self.AtomTypesStrPDB : list[str] = []

        if depth == None:
            self.depth = 10000
        self.depth = depth

    def __call__(self,tk:str, pdb:str, xyz_style:int=2 ) -> None:
        """
        Convert the tinker xyz file to pdb file
        Args:
            tk (str): The path of the tinker xyz file
            pdb (str): The path of the output pdb file
            xyz_style (int): The style of the xyz file, 1 for TinkerModellor style, 2 for Tinker style
        """


        self.read_from_tinker(tk)

        self.ResidueName = ['UNK']*self.AtomNums
        self.ResidueNum = np.zeros(self.AtomNums)

        segment_list = self._split_segement()
        #print(segment_list)
        segment_type = self._determine_segment_type(segment_list)
        
        current_residue_index = 1


        for type, index in zip(segment_type, segment_list):
            if type == 'ION':
                for i in range(index[0], index[-1]+1):
                    self.ResidueName[i] = 'ION'
                    self.ResidueNum[i] = current_residue_index
                current_residue_index += 1
            elif type == 'WAT':
                for i in range(index[0], index[-1]+1):
                    self.ResidueName[i] = 'WAT'
                    self.ResidueNum[i] = current_residue_index
                current_residue_index += 1
            else:
                if xyz_style == 1:
                    self._tkm_assign_residue(index, current_residue_index)
                elif xyz_style == 2:
                    self._tinker_assign_residue(index, current_residue_index)

        self._pdb_atomtype()

        if pdb != None:
           self.write(pdb)

    def __str__(self) -> str:
        contents = []
        
        # atoms
        for i in range(self.AtomNums):
            #print(i)
            # Format the string for each atom including its index, type, coordinates, and type number.
            # Ensure that the atom type number is aligned correctly without decimal points for integers.
            contents.append(
                f"ATOM  {i + 1:>4d} {self.AtomTypesStr[i]:<4} "
                f"{self.ResidueName[i]:>3} A "
                f"{int(self.ResidueNum[i]):4d}    "
                f"{self.AtomCrds[i, 0]:8.3f}"
                f"{self.AtomCrds[i, 1]:8.3f}"
                f"{self.AtomCrds[i, 2]:8.3f}  "
                f"1.00 15.14           {self.AtomTypesStrPDB[i]:>2}"
            )

        contents.append("END")
        return "\n".join(contents)

    def write(self, file_path):
        with open(file_path, 'w') as f:
            f.write(self.__str__())

        
    def _tkm_assign_residue(self, index:List[int], residue_index: int) -> str:
        
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

        for i in range(index[0], index[-1]+1):
            # If the atom is C-O-N, then O is the last atom in the residue
            # This is probably a peptide bond
            #print(self.AtomTypesStr[i-3], self.AtomTypesStr[i-2], self.AtomTypesStr[i-1])
            normal = i
            if self.AtomTypesStr[i-1] == 'N':
                if self.AtomTypesStr[i-3] == 'C' and self.AtomTypesStr[i-2] == 'O':

                    edge = self._clean_edges(edge, 1, i-last_residue)

                    resname = find_residue(node, edge, residue_index, i-last_residue)

                    # last_residue is the index of the first atom in the residue
                    # But ResidueName and ResidueNum are 0-indexed
                    for x in range(last_residue-1, i):
                        self.ResidueName[x] = resname
                        self.ResidueNum[x] = residue_index
                    
                    residue_index += 1

                    # Update the index of the first atom in the residue
                    last_residue = i
                    # Clear the node and edge
                    node = []
                    edge = []

            # If the atom is CTe-OTe-OTe, then the last OTe is the last atom in the residue
            if self.AtomTypesStr[i-1] == 'OTe':
                if self.AtomTypesStr[i-3] == 'CTe' and self.AtomTypesStr[i-2] == 'OTe':

                    # Add the last OTe to the node
                    node.append((normal-last_residue+1, {'element': f'{self.AtomTypesStr[normal-1][0]}'}))
                    for j in self.Bonds[normal-1]:
                        if j < normal:
                            edge.append((normal-last_residue+1, j-last_residue+1))

                    # Diffenet from the peptide bond, the last OTe is the last atom in the residue
                    # But the former process is to find the first atom in the residue (N)
                    # So i should plus 1
                    i+=1
                    edge = self._clean_edges(edge, 1, i-last_residue)

                    resname = find_residue(node, edge, residue_index, i-last_residue)

                    # last_residue is the index of the first atom in the residue
                    # But ResidueName and ResidueNum are 0-indexed
                    for i in range(last_residue-1, i-1):
                        self.ResidueName[i] = resname
                        self.ResidueNum[i] = residue_index
                    residue_index += 1

                    # Update the index of the first atom in the residue
                    last_residue = i
                    
                    # Clear the node and edge
                    node = []
                    edge = []

                else:
                    # When meet the first OTe, execute normal process
                    node.append((normal-last_residue+1, {'element': f'{self.AtomTypesStr[normal-1][0]}'}))

                    for j in self.Bonds[normal-1]:
                        if j < normal:
                            edge.append((normal-last_residue+1, j-last_residue+1))
            
            # Normal process
            else:
                node.append((normal-last_residue+1, {'element': f'{self.AtomTypesStr[normal-1][0]}'}))

                for j in self.Bonds[normal-1]:
                    if j < normal:
                        edge.append((normal-last_residue+1, j-last_residue+1))

    def _tinker_assign_residue(self, index: List[int], residue_index: int) -> str:

        find_residue = AssignResidue()
        node: List[GraphData.Node] = []
        edge: List[GraphData.Edge] = []

        last_residue = index[0]-1

        first_residue:bool = True

        element = {
            'H': 1,
            'C': 6,
            'N': 7,
            'O': 8,
            'S': 16,
        }

        i = index[0] - 1
        while i < index[-1]:

            # normal is the index of the current atom
            normal = i
            # 如果当前原子是N
            if self.AtomTypesStr[i] == 'N':
                # 检查接下来的三个原子是否为C-C-O
                if (i+3 < len(self.AtomTypesStr) and 
                    self.AtomTypesStr[i+1] == 'CA' and 
                    self.AtomTypesStr[i+2] == 'C' and 
                    self.AtomTypesStr[i+3] == 'O'):

                    if first_residue:
                        first_residue = False
                    else:
                    
                        # 处理上一个残基
                        edge = self._clean_edges(edge, 1, i-last_residue)
                        resname = find_residue(node, edge, residue_index, i-last_residue)

                        for x in range(last_residue-1, i):
                            self.ResidueName[x] = resname
                            self.ResidueNum[x] = residue_index

                        residue_index += 1

                        # 更新last_residue
                        last_residue = i
                        node = []
                        edge = []

                # 将当前N原子添加到node和edge
                node.append((normal-last_residue+1, {'element': f'{self.AtomTypesStr[normal][0]}'}))

                for j in self.Bonds[normal]:
                    if j < normal+1:
                        edge.append((j-last_residue, normal-last_residue+1))

            else:
                # 将当前原子添加到node和edge
                node.append((normal-last_residue+1, {'element': f'{self.AtomTypesStr[normal][0]}'}))

                for j in self.Bonds[normal]:
                    if j < normal+1:
                        edge.append((j-last_residue, normal-last_residue+1))

            i += 1

        # 处理最后一个残基
        edge = self._clean_edges(edge, 1, index[-1] - last_residue)
        resname = find_residue(node, edge, residue_index, index[-1] - last_residue)
        for x in range(last_residue-1, index[-1]):
            self.ResidueName[x] = resname
            self.ResidueNum[x] = residue_index
        

    def _clean_edges(self, edges:List[GraphData.Edge] , start:int , end: int) -> List[GraphData.Edge]:
        # Remove the bonds, which are not in the residue

        new_edges: List[GraphData.Edge] = []

        for edge in edges:
            atom_i, atom_2 = edge  
            if atom_i >= start and atom_i <= end and atom_2 >= start and atom_2 <= end:
                new_edges.append(edge)

        return new_edges


    def _split_segement(self):
        
        segment_list = []
        atom_index = 1

        while atom_index <= self.AtomNums:
            residule_list = self._connectivity_search(atom_index)
            segment_list.append([residule_list[0], residule_list[-1]])
            atom_index = residule_list[-1]+1
        return segment_list
    
    def _determine_segment_type(self,segment_list:List[List[int]]) -> List[str]:
        segment_type = []
        for segment in segment_list:
            start, end = segment
            if end-start+1 == 1:
                segment_type.append('ION')
            elif end-start+1 == 3:
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
        sys.setrecursionlimit(self.depth)
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
    
    def _pdb_atomtype(self):
        for i in range(self.AtomNums):
            if len(self.AtomTypesStr[i]) == 1:
                self.AtomTypesStrPDB.append(self.AtomTypesStr[i])
            else:
                if self.AtomTypesStr[i][1].islower():
                    self.AtomTypesStrPDB.append(self.AtomTypesStr[i][0:2])
                else:
                    self.AtomTypesStrPDB.append(self.AtomTypesStr[i][0])
        

if __name__ == '__main__':
        import os
        control = 2
        if control == 1:
            tk = r'example/tk2pdb/ex1/tinker.xyz'
            pdb = r'example/tk2pdb/ex1/tk2pdb.pdb'
        elif control == 2:
            tk = r'example/tk2pdb/ex2/complex.xyz'
            pdb = r'example/tk2pdb/ex2/tk2pdb.pdb'
        tk = os.path.abspath(tk)
        pdb = os.path.abspath(pdb)

        tkpdb = Tinker2PDB()
        tkpdb(tk, pdb)

        #resname = find(node, edge, 1, atom_number)
        #print(resname)
        
