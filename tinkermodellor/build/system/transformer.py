from .. import GMXSystem
from .. import TinkerSystem
from ..dataset import AmberGAFFTrans
from .. import GMXMolecule

import numpy as np

    #   This module is designed to transform the data extracted from Gromacs format files into Tinker format files.
    #   Now we only support two transformate into AMOEBABIO18 force field in Tinker format.
    #   We recommand to use Amber14sb force field and TIP3P water model which is tested successfully to build the Gromacs format files.

    #   Usage:
    #   gmx_system = GMXSystem()
    #   gmx_system.read_gmx_file('path/to/your/gromacs.gro','path/to/your/gromacs.top')
    #   transformer = Transformer()
    #   tinker_system = transformer(gmx_system)
    #   tinker_system.write('path/to/your/output.xyz')

    #   Information can be accessed as follows:
    #   tinker_system.AtomTypesStr     # List of atom types in string format for the molecule. Provides a clear understanding of the chemical nature of each atom.
    #   tinker_system.AtomTypesNum     # Numeric representations of atom types, facilitating computational analyses and comparisons.
    #   etc.
    #   For more information, please refer to the TinkerSystem class in tinkermodellor/build/system/tinker/_tinkersystem.py

class Transformer():

    def __init__(self) -> None:
        self.transformer_function = AmberGAFFTrans()

    def __call__(self,gmx_input:GMXSystem) -> TinkerSystem:
        tinker = TinkerSystem()
        self._build_tinker_system(gmx_input,tinker)
        return tinker

    def _build_tinker_system(self,gmx:GMXSystem,tinker:TinkerSystem):

        #Simple information transfer
        tinker.SystemName = gmx.SystemName
        tinker.AtomCrds = gmx.coordinates  #nm to Angstrom
        tinker.AtomNums = gmx.system_atom_nums
        tinker.BoxSize = np.array(gmx.box_size) * 10.0 #nm to Angstrom
        tinker.AtomIndex = gmx.atom_index
        self._add_by_single_molecule_type(gmx,tinker)
        #print(tinker.AtomTypesNum)
        #print(tinker.AtomTypesStr)
        #print(tinker.Bonds)
        #print(tinker.AtomCrds)

    def _add_by_single_molecule_type(self,gmx:GMXSystem, tinker:TinkerSystem) -> None:
        
        index = 1

        for i in range(1,len(gmx.moleculetype)):
            molecule_type = gmx.moleculetype[i]
            molecule_nums = int(gmx.moleculetype_num[i-1])
            molecule_name = gmx.moleculetype[i].MoleculeName

            print('\n')
            print(f"The atom index of {molecule_name} is from", index,'to',index+int(molecule_type.AtomNums)*int(molecule_nums)-1)

            for _ in range(molecule_nums):
                index = self._add_by_single_molecule(tinker,molecule_type,index)
                

       
    #Used for store each atom's atomtype, coordinates and topology
    def _add_by_single_molecule(self,tinker:TinkerSystem, molecule_type: GMXMolecule, index) -> int :

        #Transfrom the atomtype into AMEOBABIO18 force field
        num_atomtype:np.array = []
        str_atomtype = []

        for i in range(len(molecule_type.AtomTypes)):
            #DEBUG##print(element)
            #DEBUG##print(molecule_type.AtomResidue[i],molecule_type.AtomTypes[i])
            trans_type = self.transformer_function(molecule_type.AtomResidue[i],molecule_type.AtomTypes[i])
            if trans_type == 'None':
                print(f'WARNING!!! Atomtype {molecule_type.AtomTypes[i]} of Residue {molecule_type.AtomResidue[i]} not found in force field. Atom index is {i+index}')
                print('And TinerModellor has already automatically set it as "None" \n')
                num_atomtype = np.append(num_atomtype, trans_type)
                str_atomtype.append(molecule_type.AtomTypes[i])
            else:
                num_atomtype = np.append(num_atomtype, trans_type)
                str_atomtype.append(molecule_type.AtomTypes[i])

        tinker.AtomTypesNum = np.append(tinker.AtomTypesNum,num_atomtype)
        tinker.AtomTypesStr.extend(str_atomtype) 
        #DEBUG##print(len(self.AtomTypes))

        #Transform the topology into Tinker XYZ format with atom index correction
        tinker_bonds = []
        #DEBUG##print(molecule_type.Bonds)
        for element in molecule_type.Bonds[1:]:
            #element might contain more than one bond,like [1,2,10]
            corrected_bond = [int(number)+int(index)-1 for number in element[1:]] 
            tinker.Bonds.append(corrected_bond)

        
        return index + molecule_type.AtomNums

    def _check_and_trans_atomtype(self) -> None :

        #DEBUG##print(len(self.AtomTypes),len(self.AtomCrds),len(self.Bonds),self.AtomTypes[-1])
        assert len(self.Bonds) == len(self.AtomTypes) == len(self.AtomCrds), f'The length of Bonds{len(self.Bonds)}, AtomTypes({len(self.AtomTypes)}) and AtomCrds({len(self.AtomCrds)}) must be equal !'

        #The first item of AtomTypes is None, so minus 1
        self.AtomNums = len(self.AtomTypes)-1

