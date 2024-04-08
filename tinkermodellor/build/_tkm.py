from ._class._gmxmolecule import GMXMolecule
from ._class._tkm_system import TinkerModellorSystem
import re

from ._class import GMXSystem

class TinkerModellor:

    def __init__(self,aggressive:bool = True) -> None:
        """
        Used for buiding the Tinker XYZ system

        Args:
            aggressive(bool):   If true, scripts would try to pair more atom types,
                                and this may results mismatching
        """

        self.aggressive = aggressive

    def __call__(self,gro_file:str ,top_file:str):
        self.build_tkmsystem(gro_file,top_file)


    #read top file
    def _read_top_file(self,top_path:str):
        
        with open(top_path,'r') as f:
            lines=f.readlines()

        #Used for store the different molecules
        #Once read a new molecule, the it would be append to self.moleculestype.
        self.moleculetype = [GMXMolecule()]

        #To control whether the has already appeared
        molecules_flag= False

        #To record each moleculetype's number in entire system
        self.moleculetype_num = []

        #Used for counting how many moleculetypes have been read
        molecule_type_count = 0 

        #Used for counting which line is reading
        line_count = 0

        #Due to the similarity of [ bond ] and [ pairs ]
        #We must use bond_flag to determine whether it is bond or pairs
        bond_flag = False

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
                    self.moleculetype[molecule_type_count](f'TKM{molecule_type_count}',atomtype_read, atomresidue_read, bond_read)
      
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
                        atomresidue_read.append(re.sub(r'\d', '', match_atomtype.group(2)).replace(' ', ''))
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
                self.moleculetype[molecule_type_count](f'TKM{molecule_type_count}',atomtype_read, atomresidue_read, bond_read)
                molecules_flag =True

            if molecules_flag and re.fullmatch(MOLECULES_PATTERN,line):

                self.moleculetype_num.append(line.strip().split(' ')[-1])
                print(f"Detect a new molecule, and it has {self.moleculetype_num[-1]} molecules")
                
        

    def _read_gro_file(self,gro_path):

        with open(gro_path,'rt') as f:#read gro file
            lines = f.readlines()
            #To record the entire system's atom numbers
            self.system_atom_nums = int(lines[1])

        #To record the entire system's coordinates
        self.coordinates = [None]
        for line in lines[2:-1]:
            line = line.strip().split('  ')#split into 5-6 items

            #To record the entire system's coordinates
            self.coordinates.append([float(i)*10 for i in line[-3:]])



    def build_tkmsystem(self,gro_path:str, top_path:str):

        self._read_top_file(top_path)
        assert len(self.moleculetype)-1 == len(self.moleculetype_num), f'Number of Moleculetypes({len(self.moleculetype)-1}) in [ molecules ] Must Be Equal To Number({len(self.moleculetype_num)}) of [ moleculetype ]'

        self._read_gro_file(gro_path)

        self.system = TinkerModellorSystem(aggressive= self.aggressive)
        #According to self.moleculetype to rebuild the Tinker XYZ format file
        #DEBUG##print(len(self.moleculetype_num))
        count = 0
        while count < len(self.moleculetype_num):
            print('\n')
            print(f"Molecule's index is from", self.system.AtomNums+1,'to',self.system.AtomNums+self.moleculetype[count+1].AtomNums*int(self.moleculetype_num[count]))
            #DEBUG##print("moleculetype is", self.moleculetype[count+1].MoleculeName, self.moleculetype[count+1].AtomTypes)
            for i in range(int(self.moleculetype_num[count])):
                self.system(atomcrds=self.coordinates,molecule_class=self.moleculetype[count+1],atom_index=[self.system.AtomNums+1,self.system.AtomNums+self.moleculetype[count+1].AtomNums])
            count +=1
        #DEBUG##print(self.system.AtomCrds)
    
    def write_tkmsystem(self,xyz_path:str):
        self.system.write(xyz_path)

if __name__ == '__main__':


    new= TinkerModellor()
    new(r'/home/wayne/quanmol/TinkerModelling/tinkermodellor/gromacs.gro',r'/home/wayne/quanmol/TinkerModelling/tinkermodellor/gromacs.top')
