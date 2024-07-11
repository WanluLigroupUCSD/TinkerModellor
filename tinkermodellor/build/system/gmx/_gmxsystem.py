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
SYSTEM_ATOMTYPE_PATTERN = r"(\s*[0-9]+\s*)([0-9]?[a-zA-Z][0-9a-zA-Z]*-?\+?\*?)(\s*[0-9]+\s*)([0-9]?[a-zA-Z][0-9a-zA-Z]*-?\+?\s*)([0-9]?[a-zA-Z][0-9a-zA-Z]*-?\+?\s*)([0-9]+\s*-?[0-9]+\.[0-9]+\s*[0-9]+\.*[0-9]*\n?)(\s*;\s*[a-z]*\s*-?[0-9]*.[0-9]*\s*\n)?"
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
MOLECULES_PATTERN = r"(Protein_chain_[A-Z]|[A-Za-z0-9]*-?\+?)(\s*[0-9]+\n)?"

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
        #These variables are used to record the topology info
        #Used for store the different molecules，the first one is empty
        self.MoleculeType: list[GMXMolecule] = [GMXMolecule()]        
        #To record each moleculetype's number in entire system
        self.MoleculeTypeNum: list[int] = []
        #Used for store the entire system's atom numbers
        self.SystemAtomNums:int = 0

        

        
    
    @GMXSystemReminder
    def read_gmx_file(
        self,
        gro_file: str,
        top_file: str
    ) -> None:

        gro_file = os.path.abspath(gro_file)
        top_file = os.path.abspath(top_file)

        self._read_top_file(top_file)
        assert len(self.MoleculeType)-1 == len(self.MoleculeTypeNum), f'Number of Moleculetypes({len(self.MoleculeType)-1}) in [ molecules ] Must Be Equal To Number({len(self.MoleculeTypeNum)}) of [ moleculetype ]'
        self._read_gro_file(gro_file)


    def _read_top_file(self,top_path:str):
        
        with open(top_path,'r') as f:
            lines=f.readlines()
        #To control whether the has already appeared
        molecules_flag= False

        #Used for counting how many moleculetypes have been read
        molecule_type_count = 0 

        #Used for counting which line is reading
        line_count = 0

        #Due to the similarity of [ bond ] and [ pairs ]
        #We must use bond_flag to determine whether it is bond or pairs
        bond_flag = False

        #Used to search each molecule's name
        molecules_name_flag=True
        molecule_name_list = [None]
        j = -1
        while molecules_name_flag:
            if '[ molecules ]' in lines[j]:
                molecules_name_flag =False
                #print(molecule_name_list)
            elif re.fullmatch(MOLECULES_PATTERN,lines[j]):
                molecule_name_list.insert(1, lines[j].strip().split(' ')[0])

            j -=1

        molecules_count = 1
        HIS_box = []
        for line in lines:
            #A new molecule start (according to the GMX top file format)
            #GMX topology file format description: https://manual.gromacs.org/current/reference-manual/topologies/topology-file-formats.html
            line_count += 1

            if '[ moleculetype ]' in line:
                #DEBUG##print("Detect a new moleculetype")
    
                #To add items into moleculetype(GMXMolecule)
                if molecule_type_count > 0:
                    #print(atomtype_read)
                    #print(molecule_type_count)
                    #print(bond_read)
                    #print(molecule_type_count,molecule_name_list[molecule_type_count])
                    self.MoleculeType[molecule_type_count](f'{molecule_name_list[molecule_type_count]}',atomtype_read, atomresidue_read, bond_read)
      
                #Build a new GMXMolecule class to store a new moleculetype
                molecule_type_count += 1
                self.MoleculeType.append(GMXMolecule())    
                atomtype_read = []
                bond_read = []
                atomresidue_read = []
                continue

            #Only when the molecule type is not empty, the program would read the information
            if molecule_type_count > 0 and molecules_flag == False:
                
                #To match the ATOMTYPE_PATTE
                match_atomtype = re.fullmatch(SYSTEM_ATOMTYPE_PATTERN,line)
                if match_atomtype:
                    ligand_atomtype =re.fullmatch(LIGAND_ATOMTYPE_PATTERN,line)
                    if ligand_atomtype:
                        atomtype_read.append(ligand_atomtype.group(2).replace(' ', ''))
                        atomresidue_read.append(re.sub(r'\d', '', match_atomtype.group(4)).replace(' ', ''))
                        #DEBUG##print(line)
                    else:
                        temp_atomtype = match_atomtype.group(5)[:4].replace(' ', '')
                        temp_atomresidue = re.sub(r'\d', '', match_atomtype.group(4)).replace(' ', '')
                        
                        # CYS and CYX has the same SG , the only difference is that CYX has no H atom
                        # two paths to deal with the problem
                        # 1: divide residue into CYS and CYX via HG 2: divide atomtype into SG and SGH via HG 
                        # we choose the second one , however CYX is also avaliable
                        if temp_atomresidue == 'CYS' and temp_atomtype == 'HG':
                            atomtype_read.pop()#remove restored SG
                            atomtype_read.append('SGH')#mark it and append , see dataset/amoebabio/_amber.py
                            atomtype_read.append('HG')#normal append

                        elif temp_atomresidue == 'HIS':
                            # HIS has three types,HISE(HE2) HISD(HD1), HISH(HE2,HD1) , the read order is {HD1>HE2}
                            # so if read HE2 , the residue is HISE or HISH ,just check if HD1 is in HIS_box
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
                                atomresidue_read.extend([residue]*len(HIS_box))
                                HIS_box = []
           
                        #this is common path
                        else:
                            atomtype_read.append(temp_atomtype)
                        
                        #Residue name in GMX top file is not always the same as the residue name in Tinker XYZ file
                        if temp_atomresidue != "HIS":
                            atomresidue_read.append(temp_atomresidue)
                        



                #DEBUG##print(atomresidue_read)
                #DEBUG##print(atomtype_read)

                #To match the BOND_PATTERN
                if '[ bonds ]' in line:
                    bond_flag = True
                if not line.strip():
                    bond_flag = False 

                #match_bond = re.fullmatch(BOND_PATTERN,line)
                if bond_flag and ';' not in line and '[ bonds ]' not in line:
                    #DEBUG##print(line)
                    #DEBUG##print(line_count)
                    bond_line = line.strip().split()
                    bond_read.append([int(bond_line[0]),int(bond_line[1])])
                    #bond_read.append([int(match_bond.group(1)),int(match_bond.group(2))])
            
            
            if '[ molecules ]' in line:
                self.MoleculeType[molecule_type_count](f'{molecule_name_list[molecule_type_count]}',atomtype_read, atomresidue_read, bond_read)
                molecules_flag =True
            
            
            if molecules_flag and re.fullmatch(MOLECULES_PATTERN,line):
                self.MoleculeTypeNum.append(line.strip().split(' ')[-1])
                print(f"Detect a new molecule, and it has {self.MoleculeTypeNum[-1]} molecules, its name is {self.MoleculeType[molecules_count].MoleculeName} and it consists of {self.MoleculeType[molecules_count].AtomNums} atoms.\n")
                molecules_count += 1

    def _read_gro_file(self,gro_path):

        with open(gro_path,'rt') as f:#read gro file
            lines = f.readlines()
            #To record the entire system's atom numbers
            self.SystemAtomNums = int(lines[1])

        for line in lines[2:-1]:
            line = line.strip().split('  ')#split into 5-6 items

            #To record the entire system's coordinates
            self.Coordinates.append(np.array([float(i)*10 for i in line[-3:]]))
        self.AtomIndex = np.arange(1, len(self.Coordinates))
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