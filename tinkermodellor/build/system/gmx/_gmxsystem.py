import re
import os
import numpy as np
from dataclasses import dataclass

from ._gmxmolecule import GMXMolecule
from ....messager import GMXSystemReminder

#This is the regular expression for specific part in topology file

#this is the regular expression for capturing the charge part in protein top file
#but protein top file has two different patterns for charge part
#(ions&water)              1                  Na+                           1                 Na+                Na+                1            1.00000000        22.990000                        ; qtot 1.000000
#(ligand)                  1                  ca                            1                 MOL                C                  1            0.00000000        12.010736
#(protein)                33                  C                           248                 GLU                C                 33            0.5366            12.01
#(protein)                34                  O                           248                 GLU                O                 34           -0.5819            16                               ; qtot 0
#                      <----------------------------------grp 1----------------------> <----- grp 2 -----> <--- grp 3 ---><-------------------------------- grp 4 ----------------------------------->
#
#SYSTEM_ATOMTYPE_PATTERN = r"(\s*[0-9]+\s*)([0-9]?[a-zA-Z][0-9a-zA-Z]*-?\+?\*?)(\s*[0-9]+\s*)([0-9]?[a-zA-Z][0-9a-zA-Z]*-?\+?\s*)([0-9]?[a-zA-Z][0-9a-zA-Z]*-?\+?\s*)([0-9]+\s*-?[0-9]+\.[0-9]+\s*[0-9]+\.*[0-9]*\n?)(\s*;\s*[a-z]*\s*-?[0-9]*.[0-9]*\s*\n)?"
SYSTEM_ATOMTYPE_PATTERN = r"(\s*[0-9]+\s*)(-?[0-9]?[a-zA-Z][0-9a-zA-Z]*-?\+?\*?)(\s*[0-9]+\s*)([0-9]?[a-zA-Z][0-9a-zA-Z]*[-\+\']?\d*\s*)([0-9]?[a-zA-Z][0-9a-zA-Z]*[-\+\']?\d*\s*)([0-9]+\s*-?[0-9]+\.[0-9]+\s*[0-9]+\.*[0-9]*\n?)(\s*;\s*[a-z]*\s*-?[0-9]*.[0-9]*\s*\n)?"
LIGAND_ATOMTYPE_PATTERN = r'(\s*[0-9]+\s*)([0-9a-z]*)(\s*[0-9]+)(\s*[a-zA-Z][0-9a-zA-Z]*)(\s*[0-9]?[a-zA-Z][0-9a-zA-Z]*-?\+?)(\s*[0-9]+\s*-?[0-9]+\.[0-9]+\s*[0-9]+\.*[0-9]*)(\s*;\s*[a-z]*\s*-?[0-9]*.[0-9]*\s*\n)?'

#[ bonds ]
#;                    ai          aj     funct         c0         c1         c2         c3
#                     17          20     1            0.14650 272713.120000
#                 <-- grp 1 --><grp 2 ><---------------grp 3--------------->
BOND_PATTERN = r"\s*([0-9]+)\s*([0-9]+)(\s*1)(\s*[0-9].[0-9]*\s*[0-9]*.[0-9]*\n?)?(\s*[0-9].[0-9]*\s*[0-9]*.[0-9]*\n)?"

#[ molecules ]
#;                     Compound               mols
#                      system1                1
#                      Na+                    10
#                      WAT                    9971
#                 <-------- grp 1 ---------><grp 2 >
#MOLECULES_PATTERN = r"(Protein_chain_[A-Z]|[A-Za-z0-9]*-?\+?)(\s*[0-9]+\n)?"
MOLECULES_PATTERN = r"([A-Za-z0-9_]*-?\+?)(\s*[0-9]+\n)?"
NAME_PATTERN = r"([A-Za-z0-9]*-?\+?)(\s*[0-9]+\n)?"

@dataclass
class GMXSystem():
    #This module is designed to store the key information from Gromacs Format file(including .gro .top file)
    #Usage: 
    #   gmx = GMXSystem()
    #   gmx.read_gmx_file(gro_file = r'gromacs.gro', top_file = r'gromacs.top')

    #information for each moleculetype:
    #   gmx.MoleculeType[1].AtomTypes       #The atom type list for atom in this molecule  (gmx.MoleculeType[1] is the first moleculetype in the system and gmx.MoleculeType[0] is empty)
    #   gmx.MoleculeType[1].Bonds           #The bond list for atom in this molecule (for connectivity recognition)
    #   gmx.MoleculeType[1].AtomNums        #The number of atoms in this molecule
    #   gmx.MoleculeType[1].AtomResidue     #The residue name for atom in this molecule
    #   gmx.MoleculeType[1].MoleculeName    #The name of this molecule
    
    #information for entire system:
    #   gmx.MoleculeTypeNum                 #The number of each moleculetype in the system
    #   gmx.Coordinates                     #The coordinates of the entire system (first one is empty)
    #   gmx.SystemAtomNums                  #The atom numbers of the entire system
    #   gmx.BoxSize                         #The box size of the entire system  (default is 0,0,0)
    #   gmx.BoxAngles                       #The box angle of the entire system (default is 90,90,90)

    def __init__(self, system_name :str = None) -> None:
        if system_name is None:
            self.SystemName = 'TinkerModellorSystem'
        else:
            self.SystemName = system_name
        
        #Used for store the atom index
        self.AtomIndex: np.array = []
        #These variables are used to record the box information
        self.BoxSize:np.array = [0,0,0]
        self.BoxAngles:np.array = [90,90,90]
        #These variables are used to record the coordination info
        #To record the entire system's coordinates
        self.Coordinates: np.array = [] # Nanometer
        #the self.MoleculeType: dict[str:GMXMolecule] is used to record the topology of molecule which will be used to build the system
        #In other words, the molecule types used in system must be recorded in self.MoleculeType 
        self.MoleculeTypes: dict[str:GMXMolecule] = {}        
        #Used for store the entire system's atom numbers
        self.SystemAtomNums:int = 0
        #Used for store the number of each molecule type in the system
        self.MoleculeOrder:list[tuple[str,int]] = []

        

        
    
    @GMXSystemReminder
    def read_gmx_file(
        self,
        gro_file: str,
        top_file: str
    ) -> None:

        gro_file = os.path.abspath(gro_file)
        top_file = os.path.abspath(top_file)

        self._read_top_file(top_file)
        #assert len(self.MoleculeTypes)-1 == len(self.MoleculeTypeNum), f'Number of Moleculetypes({len(self.MoleculeTypes)-1}) in [ molecules ] Must Be Equal To Number({len(self.MoleculeTypeNum)}) of [ moleculetype ]'
        self._read_gro_file(gro_file)


    def _read_top_file(self, top_path: str):
        with open(top_path, 'r') as f:
            total_lines_of_gro_file = f.readlines()
        molecules_flag = False
        #molecule_type_count = 0
        line_count = 0
        bond_flag = False
        molecules_flag = True
        single_molecule_name_flag = True
        reverse_index = -1

        #this loop is used to find the molecules name from bottom to top
        #it will stop until find the title of [ molecules ]
        while molecules_flag:
            if '[ molecules ]' in total_lines_of_gro_file[reverse_index]:
                molecules_flag = False
                #the molecules_flag switch to False to end the loop
            elif re.fullmatch(MOLECULES_PATTERN, total_lines_of_gro_file[reverse_index]):
                #insert will add the molecules name to the first place
                #the dict record the molecules name and the number to instruct building the system
                element = list(filter(None,total_lines_of_gro_file[reverse_index].strip().split(' ')))
                molecule_name = element[0]
                molecule_num = int(element[1])
                #this part fix the order
                self.MoleculeOrder.insert(0,(molecule_name,molecule_num))
            reverse_index -= 1
        
        #print(molecules_in_system)

        #molecules_count = 1
        HIS_box = []
        for line in total_lines_of_gro_file:
            line_count += 1
            #line = line
            if '[ moleculetype ]' in line:
                if len(self.MoleculeTypes) > 0:
                    #IF the self.MoleculeType is not empty
                    #then it will exert the GMXMolecule.__init__() to build the molecule
                    #I should point that a molecule will be build when the next [ moleculetype ] title is read
                    #print(self.MoleculeTypes)
                    #print(molecule_name,len(atomtype_read))
                    self.MoleculeTypes[molecule_name](molecule_name, atomtype_read, atomresidue_read, bond_read)
                
                #former_start
                #A GMXMolecule() will be add to self.MoleculeType when read the [ moleculetype ] title 
                #however the GMXMolecule() in self.MoleculeType can only be distinguished by the index
                #former_end

                #all attributes of GMXMolecule() will be init when read the [ moleculetype ] title 
                #molecule_type_count += 1
                atomtype_read = []
                bond_read = []
                atomresidue_read = []
                single_molecule_name_flag = True
                continue
            
            if single_molecule_name_flag:
                #now
                #I tried to record the molecule type name in self.MoleculeType to make it easier to distinguish
                #And a new GMXMolecule() will be added to self.MoleculeType which is pair to the molecule name
                match_name = re.fullmatch(NAME_PATTERN, line)
                if match_name:
                    molecule_name = match_name.group(1)
                    self.MoleculeTypes[molecule_name] = GMXMolecule()
            if '[ atoms ]' in line:
                single_molecule_name_flag = False


            if len(self.MoleculeTypes) > 0 and not molecules_flag:
                match_atomtype = re.fullmatch(SYSTEM_ATOMTYPE_PATTERN, line)
                if match_atomtype:
                    ligand_atomtype = re.fullmatch(LIGAND_ATOMTYPE_PATTERN, line)
                    if ligand_atomtype:
                        atomtype_read.append(ligand_atomtype.group(2).replace(' ', ''))
                        atomresidue_read.append(re.sub(r'\d', '', match_atomtype.group(4)).replace(' ', ''))
                    else:
                        temp_atomtype = match_atomtype.group(5)[:4].replace(' ', '')
                        temp_atomresidue = re.sub(r'\d', '', match_atomtype.group(4)).replace(' ', '')

                        if temp_atomresidue == 'CYS' and temp_atomtype == 'HG':
                            atomtype_read.pop()
                            atomtype_read.append('SGH')
                            atomtype_read.append('HG')

                        elif temp_atomresidue == 'HIS':
                            HIS_box.append(temp_atomtype)
                            atomtype_read.append(temp_atomtype)

                            if temp_atomtype == 'O':
                                if 'HE2' in HIS_box:
                                    if 'HD1' in HIS_box:
                                        residue = "HISH"
                                    else:
                                        residue = "HISE"
                                else:
                                    residue = "HISD"
                                atomresidue_read.extend([residue] * len(HIS_box))
                                HIS_box = []
                        #although the is existing a Terminal check mechanism,
                        #but it not work for the terminal of RNA&DNA
                        #another check of the atomtype was applied to solve this problem
                        #however the PO3' are not considered
                        #since the relavant atoms are defined as -1 in tinker
                        elif temp_atomtype == "H5T" :
                            atomtype_read.pop()
                            atomtype_read.append("O5'T")
                            atomtype_read.append("H5T")

                        elif temp_atomtype == "H3T" :
                            atomtype_read.pop()
                            atomtype_read.append("O3'T")
                            atomtype_read.append("H3T")

                        else:
                            atomtype_read.append(temp_atomtype)

                        if temp_atomresidue != "HIS":
                            atomresidue_read.append(temp_atomresidue)


                if '[ bonds ]' in line:
                    bond_flag = True
                if not line.strip():
                    bond_flag = False

                if bond_flag and ';' not in line and '[ bonds ]' not in line:
                    bond_line = line.strip().split()
                    bond_read.append([int(bond_line[0]), int(bond_line[1])])
            
            #
            if '[ molecules ]' in line:
                #when read the [ molecules ] for the second time
                #it means that all the molecules have been read
                #the last molecule will be bulit
                self.MoleculeTypes[molecule_name](molecule_name, atomtype_read, atomresidue_read, bond_read)
                molecules_flag = True

            '''
            if molecules_flag and re.fullmatch(MOLECULES_PATTERN, line):
                #finally sort and check
                self.MoleculeTypeNum.append(line.strip().split(' ')[-1])
                if molecules_count < len(self.MoleculeType):
                    print(f"Detect a new molecule, and it has {self.MoleculeTypeNum[-1]} molecules, its name is {self.MoleculeType[molecules_count].MoleculeName} and it consists of {self.MoleculeType[molecules_count].AtomNums} atoms.\n")
                else:
                    print(f"Error: Molecule count {molecules_count} exceeds MoleculeType length {len(self.MoleculeType)}.")
                molecules_count += 1
            '''
            if molecules_flag :
                #finally sort and check
                for molecule_name_num in self.MoleculeOrder:
                    molecule_name = molecule_name_num[0]
                    certain_molecule = self.MoleculeTypes.get(molecule_name,None)
                    if certain_molecule is None:
                        raise ValueError(f"Error: Molecule {molecule_name} not found in MoleculeTypes{self.MoleculeTypes}.")
                    else:pass



    def _read_gro_file(self,gro_path):

        with open(gro_path,'rt') as f:#read gro file
            lines = f.readlines()
            #To record the entire system's atom numbers
            self.SystemAtomNums = int(lines[1])

        for line in lines[2:-1]:
            line = line.strip().split()#split into 5-6 items
            #To record the entire system's coordinates
            self.Coordinates.append(np.array([float(i)*10 for i in line[-3:]]))
        self.AtomIndex = np.arange(1, len(self.Coordinates)+1)
        self.Coordinates = np.array(self.Coordinates)

        #read box size
        box_flag=True
        j = -1
        while box_flag:
            if not lines[j].strip():
                pass
            else:
                numbers = map(float, lines[j].split())
                rounded_numbers = [round(num, 5) for num in numbers]
                self.BoxSize = rounded_numbers
                box_flag = False

            j -=1