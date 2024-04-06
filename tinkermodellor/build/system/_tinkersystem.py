from ._gmxmolecule import GMXMolecule
from typing import List, Union
from ..para_trans.amoebabio18._forcefieldtrans import AmberGAFFTrans


class TinkerModellorSystem() :
        
    def __init__(self, aggressive:bool = True, name:str = None) -> None :
        """
        Used for store the molecule information (Tinker XYZ format)

        Args:
            aggressive(bool):   If true, scripts would try to pair more atom types,
                                and this may results mismatching
        """
        #Used for store the molecular type
        self.AtomTypes: list[str] = [None]
        #Used for store the molecular bond
        self.Bonds: Union[List[int], List[str]] = [None]
        #Used for store the molecule Numbers
        self.AtomNums: int = 0
        #Used for store the molecule coordinates
        self.AtomCrds: Union[List[float],List[str]] = [None]
        #Used for store the original atomtypes(string,like CA, n8, OW, etc.)
        self.AtomTypesOriginal: list[str] = [None]
        #Used for store the residue name
        self.ResidueName: str = [None]
        
        #Used for store the atomtype transformation (into AMEOBABIO18 force field)
        if aggressive == True:
            print('\nAggressive mode is on, this may results atomtype mismatching')
        self.trans = AmberGAFFTrans(Aggressive=aggressive)

        #Set entire system's name
        if name == None:
            self.MoleculeName = 'TinkerModellor Default Name'

        else:
            if isinstance(name,str):
                self.MoleculeName = name
            else:
                raise TypeError('MoleculeName must be a string')
            
    def __call__(self, name: str ='TinkerModellor Default Name', 
                atomcrds: Union[List[float],List[str]] = None,
                molecule_class: GMXMolecule() = None,
                atom_index: list[int] = None) -> None :
        """
        Construct the Tinker XYZ format system
        Args:
            name(str):              The name of the system
            atomcrds(list):         The coordinates of the system
            molecule_class(GMXMolecule()):  The molecule class
            ato,_index(list):       The index of the atom in the system

        Returns:
            None
        """
        assert isinstance(molecule_class,GMXMolecule), 'molecule_class or molecule_index must be provided'
        assert isinstance(atom_index,list), 'molecule_class or molecule_index must be provided'
        assert isinstance(atomcrds,list), 'atomcrds must be a list'

        self._get_top_and_crd(molecule_class,atom_index,atomcrds)
        #DEBUG##print(molecule_class.AtomResidue)
        self._check_and_trans_atomtype()
       
    #Used for store each atom's atomtype, coordinates and topology
    def _get_top_and_crd(self, molecule_class: GMXMolecule(), molecule_index: list[int,int],atomcrds: Union[List[float],List[str]]) -> None :

        #Transfrom the atomtype into AMEOBABIO18 force field
        num_atomtype = []
        str_atomtype = []
        for i in range(len(molecule_class.AtomTypes)):
            #DEBUG##print(element)
            #DEBUG##print(molecule_class.AtomResidue[i],molecule_class.AtomTypes[i])
            trans_type = self.trans(molecule_class.AtomResidue[i],molecule_class.AtomTypes[i])
            if trans_type == 'None':
                print(f'WARNING!!! Atomtype {molecule_class.AtomTypes[i]} of Residue {molecule_class.AtomResidue[i]} not found in force field')
                print('And TinerModellor has already automatically set it as "None" \n')
                num_atomtype.append(trans_type)
                str_atomtype.append(molecule_class.AtomTypes[i])
            else:
                num_atomtype.append(trans_type)
                str_atomtype.append(molecule_class.AtomTypes[i])
        self.AtomTypes += num_atomtype
        self.AtomTypesOriginal += str_atomtype
        #DEBUG##print(len(self.AtomTypes))

        #Transform the topology into Tinker XYZ format with atom index correction
        tinker_bonds = []
        #DEBUG##print(molecule_class.Bonds)
        for element in molecule_class.Bonds[1:]:
            #element might contain more than one bond,like [1,2,10]
            corrected_bond = []
            for number in element[1:]:
                corrected_bond.append([int(number)+int(self.AtomNums)]) 
            tinker_bonds.append(corrected_bond)
        self.Bonds += tinker_bonds

        #int(molecule_index[1])+1 : plus extra 1 is to make sure list contains the last index
        self.AtomCrds += atomcrds[int(molecule_index[0]):int(molecule_index[1])+1]
        
    def _check_and_trans_atomtype(self) -> None :

        #DEBUG##print(len(self.AtomTypes),len(self.AtomCrds),len(self.Bonds),self.AtomTypes[-1])
        assert len(self.Bonds) == len(self.AtomTypes) == len(self.AtomCrds), f'The length of Bonds{len(self.Bonds)}, AtomTypes({len(self.AtomTypes)}) and AtomCrds({len(self.AtomCrds)}) must be equal !'

        #The first item of AtomTypes is None, so minus 1
        self.AtomNums = len(self.AtomTypes)-1

    def write(self,xyz_path:str):
        """
        Write the Tinker XYZ format file

        Args:
            xyz_path(str):  The path of the Tinker XYZ format file

        Returns:
            None
        """
        with open(xyz_path,'wt') as f:
            f.write(f' {self.AtomNums}   Generated by TinkerModellor, Author:Xujian Wang & Haodong Liu\n')
            for i in range(1,len(self.AtomTypes)):
                bonds_str = '   '.join(str(bond[0]) for bond in self.Bonds[i])
                f.write('{:>6}{:>5}{:>15.6f}{:>12.6f}{:>12.6f} {:>5}      {}\n'.format(i, self.AtomTypesOriginal[i], self.AtomCrds[i][0], self.AtomCrds[i][1], self.AtomCrds[i][2], self.AtomTypes[i], bonds_str))