from typing import  List, Union
from dataclasses import dataclass


@dataclass
class GMXMolecule() :
    #This module is designed to store the key information from Gromacs Format file(including .gro .top file)
    #But this is designed to store a single molecular type (like protein, water, ligand)
    #As for entire system information, it is build in the GMXSystem
    #GMX format: https://manual.gromacs.org/current/reference-manual/topologies/topology-file-formats.html
    
    n_terminal_atomtype = ['N','NH']
    c_terminal_atomtype = ['C']
    c_terminal_atomtype_for_oxygen = ['OXT','OC1','OC2','O']

    #Used for store the residue name list
    residue_list =  [
        "ALA", "ARG", "ASN", "ASP", "CYS",
        "GLN", "GLU", "GLY", "HIE", "ILE",
        "LEU", "LYS", "MET", "PHE", "PRO",
        "SER", "THR", "TRP", "TYR", "VAL","HIS"]
    
    def __init__(self, molecule_name:str = None) -> None :
        #Used for store the molecule information

        #Used for store the molecular name
        if molecule_name is None:
            self.MoleculeName = 'TinkerModellorMolecule'
        else:
            self.MoleculeName = molecule_name
            
        #Used for store the molecular type
        self.AtomTypes: list[str] = []
        #Used for store the molecule Numbers
        self.AtomNums: int = 0
        #Used for store the molecule residue name
        self.AtomResidue: list[str] = []
        #Used for store the molecular bond
        self.Bonds: Union[List[int,int], List[str,str]] = []

    def __call__(self, 
                 name: str, 
                 atomtypes: List[str],
                 atomeresiudes: List[str],
                 bonds: Union[List[int], List[str]]) -> None :
        """
        Construct the molecule

        Args:
            name(str):          The name of the molecule
            atomtypes(list):    The atom types of the molecule
            bonds(list):        The bonds of the molecule, used for determine the molecule's topology
            atomcrds(list):     The coordinates of the molecule

        Returns:
            None
        """
        self._get_moleculename(name)
        self._get_atomtypes_and_residues(atomtypes,atomeresiudes)
        self._get_bonds(bonds)
        self._terminal_check()
        self._check()

    def _get_moleculename(self, name: str) -> None :
        if isinstance(name,str):
            self.MoleculeName = name
        else:
            raise TypeError('MoleculeName must be a string')
        
    def _get_atomtypes_and_residues(self, atomtypes: List[str], atomresidues:List[str]) -> None :
        
        if isinstance(atomtypes,list):
            self.AtomTypes += atomtypes
            #DEBUG##print(self.AtomTypes)
        else:
            raise TypeError('AtomTypes must be a string list')
        
        if isinstance(atomresidues,list):
            self.AtomResidue += atomresidues
        else:
            raise TypeError('AtomResidue must be a string list')
        
    def _get_bonds(self, bonds: Union[List[int], List[str]]) -> None :
        if isinstance(bonds,List):
            #create a list for each atom, the index is atom's index, the value is the index of the atom which is bonded to this atom
            list = [[[]] for _ in range(len(self.AtomTypes)+1)]
            #DEBUG##print(len(self.AtomTypes))

            #take value from bonds(list), and use the value as the index of list, then append the index of the value to the list
            for i in range(len(bonds)):
                #DEBUG##print(bonds)
                #print(i)
                list[int(bonds[i][0])].append(int(bonds[i][1]))
                list[int(bonds[i][1])].append(int(bonds[i][0]))

            #store the list to self.Bonds
            #print(list)
            self.Bonds = list
        else:
            raise TypeError('Bonds must be a int or str list')

    def _terminal_check(self) -> None :

        #Only when the molecule is protein, the terminal check is needed
        if self.AtomResidue[0] != self.AtomResidue[-1] or len(self.AtomResidue) > 100:

            #To determine whether it is a protein with normal residue name
            if self.AtomResidue[0].strip().upper() in GMXMolecule.residue_list:
                n_terminal = self.AtomResidue[0]
            else:
                print("The first residue name is "+ self.AtomResidue[0])
                print(f"{self.MoleculeName} is not a protein with regular residue name, TinkerModellor wont do residue terminal check! \n")
                return 
            
            if self.AtomResidue[-1].strip().upper() in GMXMolecule.residue_list:
                c_terminal = self.AtomResidue[-1]
            else:
                print("The last residue name is "+ self.AtomResidue[-1])
                print(f"{self.MoleculeName} is not a protein with regular residue name, TinkerModellor wont do residue terminal check!\n")
                return
            
            print(f"{self.MoleculeName} is a protein with regular residue name, TinkerModellor will do residue terminal check!\n")

            #N terminal check and atomtype replace
            if n_terminal:
                terminal_count = 0
                first_n:bool = False
                while not first_n :
                    if self.AtomTypes[terminal_count] in GMXMolecule.n_terminal_atomtype:
                        self.AtomTypes[terminal_count] = 'NTe'
                        first_n = True
                    terminal_count += 1
            
            if c_terminal:
                terminal_count = -1
                last_c:bool = False

                #C terminal contains 1 Carbon atom and 2 Oxygen atoms
                three_atom_count = 0
                while not last_c :
                    if self.AtomTypes[terminal_count] in GMXMolecule.c_terminal_atomtype:
                        self.AtomTypes[terminal_count] = 'CTe'
                        three_atom_count +=1
                    if self.AtomTypes[terminal_count] in GMXMolecule.c_terminal_atomtype_for_oxygen:
                        self.AtomTypes[terminal_count] = 'OTe'
                        three_atom_count +=1
                    if three_atom_count == 3:
                        last_c =True

                    terminal_count -= 1

    def _check(self) -> None :
        assert len(self.Bonds) == len(self.AtomTypes)+1, f'The length of Bonds({len(self.Bonds)}), AtomTypes({len(self.AtomTypes)+1}) and AtomCrds must be equal !'
        self.AtomNums = len(self.AtomTypes)


