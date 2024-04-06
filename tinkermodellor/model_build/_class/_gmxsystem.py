import re
import os

from ._gmxmolecule import GMXMolecule
from ...messager import GMXSystemReminder

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

class GMXSystem():
    #This module is designed to store the key information from Gromacs Format file(including .gro .top file)
    #Usage: 
    #   gmx = GMXSystem()
    #   gmx.read_gmx_file(r'gromacs.gro',r'gromacs.top')

    #information for each moleculetype:
    #   gmx.moleculetype[1].AtomTypes       #The atom type list for atom in this molecule  (gmx.moleculetype[1] is the first moleculetype in the system and gmx.moleculetype[0] is empty)
    #   gmx.moleculetype[1].Bonds           #The bond list for atom in this molecule (for connectivity recognition)
    #   gmx.moleculetype[1].AtomNums        #The number of atoms in this molecule
    #   gmx.moleculetype[1].AtomResidue     #The residue name for atom in this molecule
    #   gmx.moleculetype[1].MoleculeName    #The name of this molecule
    
    #information for entire system:
    #   gmx.moleculetype_num                #The number of each moleculetype in the system
    #   gmx.coordinates                     #The coordinates of the entire system (first one is empty)
    #   gmx.system_atom_nums                #The atom numbers of the entire system
    #   gmx.box_size                        #The box size of the entire system  (default is 0,0,0)
    #   gmx.box_angle                       #The box angle of the entire system (default is 90,90,90)

    def __init__(self, system_name :str = None) -> None:
        if system_name is None:
            self.SystemName = 'TinkerModellorSystem'
        else:
            self.SystemName = system_name

        #These variables are used to record the topology info
        #Used for store the different molecules，the first one is empty
        self.moleculetype = [GMXMolecule()]        
        #To record each moleculetype's number in entire system
        self.moleculetype_num = []

        #These variables are used to record the coordination info
        #To record the entire system's coordinates
        self.coordinates = [None]
        self.system_atom_nums = 0

        #These variables are used to record the box information
        self.box_size = [0,0,0]
        self.box_angle = [90,90,90]
    
    @GMXSystemReminder
    def read_gmx_file(self,gro_file:str ,top_file:str):

        gro_file = os.path.abspath(gro_file)
        top_file = os.path.abspath(top_file)

        self._read_top_file(top_file)
        assert len(self.moleculetype)-1 == len(self.moleculetype_num), f'Number of Moleculetypes({len(self.moleculetype)-1}) in [ molecules ] Must Be Equal To Number({len(self.moleculetype_num)}) of [ moleculetype ]'
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
                    self.moleculetype[molecule_type_count](f'{molecule_name_list[molecule_type_count]}',atomtype_read, atomresidue_read, bond_read)
      
                #Build a new GMXMolecule class to store a new moleculetype
                molecule_type_count += 1
                self.moleculetype.append(GMXMolecule())    
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

                        #In CYS, S in both of S-S or S-H is defined as SG in GMX top file, but in Tinker XYZ file, S in S-S is defined as SGS
                        if temp_atomresidue == 'CYS' and temp_atomtype == 'S':
                            atomtype_read.append('SGS')
                        else:
                            atomtype_read.append(temp_atomtype)
                        
                        #Residue name in GMX top file is not always the same as the residue name in Tinker XYZ file
                        atomresidue_read.append(temp_atomresidue)
                        
                        #DEBUG##print(line)

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
                self.moleculetype[molecule_type_count](f'{molecule_name_list[molecule_type_count]}',atomtype_read, atomresidue_read, bond_read)
                molecules_flag =True
            
            
            if molecules_flag and re.fullmatch(MOLECULES_PATTERN,line):
                self.moleculetype_num.append(line.strip().split(' ')[-1])
                print(f"Detect a new molecule, and it has {self.moleculetype_num[-1]} molecules, its name is {self.moleculetype[molecules_count].MoleculeName} and it consists of {self.moleculetype[molecules_count].AtomNums} atoms.\n")
                molecules_count += 1

    def _read_gro_file(self,gro_path):

        with open(gro_path,'rt') as f:#read gro file
            lines = f.readlines()
            #To record the entire system's atom numbers
            self.system_atom_nums = int(lines[1])

        for line in lines[2:-1]:
            line = line.strip().split('  ')#split into 5-6 items

            #To record the entire system's coordinates
            self.coordinates.append([float(i)*10 for i in line[-3:]])
        
        #read box size
        box_flag=True
        j = -1
        while box_flag:
            if not lines[j].strip():
                pass
            else:
                numbers = map(float, lines[j].split())
                rounded_numbers = [round(num, 5) for num in numbers]
                self.box_size = rounded_numbers
                box_flag = False

            j -=1