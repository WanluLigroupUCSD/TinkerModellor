from ._abc import FroceFieldTrans
from ._json_loader import JsonLoader
from .amoebabio09 import AMOEBABIO09ForceFieldDict
from .amoebabio18 import AMOEBABIO18ForceFieldDict
from .amoebapro13 import AMOEBAPRO13ForceFieldDict

class AmberTrans(FroceFieldTrans):
    
    def __init__(self,ForceField:str = '1'):
        """
        Force Field Transformation Dictionary Initialization

        Args:
            ForceField (int, optional): The force field type. Defaults to 1 (AMOEBABIO18).
            
        """
        
        super().__init__()
        self.ForceField = ForceField if ForceField not in ['1','2','3','4'] else int(ForceField)
        #Preparation for the abnormal(water/ions/ligand)force field transformation
        self.FFParameter: dict = {}
        #Preparation for the normal(amino acid)force field transformation
        self.ForceFieldDict: dict[str, dict[str, int]] = {}

        #PRT is defined in AMOEBA force field as the terminal proline
        self.ResidueList: list[str] =  [
            "ALA", "ARG", "ASN", "ASP", "CYS",
            "GLN", "GLU", "GLY", "HIE", "ILE",
            "LEU", "LYS", "MET", "PHE", "PRO",
            "SER", "THR", "TRP", "TYR", "VAL",
            "HISD","HISE","HISH","LYSN","GLUH",
            "ASPH","CYX","TYRA","HID","HIE",
            "HIP","PRT"]
        
        self.NAandWATList: list[str] = ["DA","DC","DG","DT","A","C","G","U","SOL","WAT"]

        support_forcefield = []

        if self.ForceField == 1:
            from .amoebabio18 import WaterAndIonsForceField
            self.ForceFieldDict = AMOEBABIO18ForceFieldDict._Amberpara
            support_forcefield=[WaterAndIonsForceField.ion_para,WaterAndIonsForceField.water_para]
        elif self.ForceField == 2:
            from .amoebabio09 import WaterAndIonsForceField
            self.ForceFieldDict = AMOEBABIO09ForceFieldDict._Amberpara
            support_forcefield=[WaterAndIonsForceField.ion_para,WaterAndIonsForceField.water_para]
        elif self.ForceField == 3:
            from .amoebapro13 import WaterAndIonsForceField
            self.ForceFieldDict = AMOEBAPRO13ForceFieldDict._Amberpara
            support_forcefield=[WaterAndIonsForceField.ion_para,WaterAndIonsForceField.water_para]
        
        Loader = JsonLoader()
        self.NAandWATForceFieldDict = Loader.load_json(self.ForceField)
    

        #Update the force field transformation dictionary
        for i in support_forcefield:self.FFParameter.update(i)


    def __call__(self,atom_residue:str, atom_type: str) -> str:
        return self._transform_to_tinker(atom_type,atom_residue)        
    

    def _transform_to_tinker(self, atom_type: str, atom_residue: str) -> str:
    
        #To check whether the residue is normal residue
        #Normal residue: LYS, ARG, GLU, etc.
        if atom_residue in self.ResidueList:
            return self.get_atom_type(self.ForceFieldDict,atom_residue, atom_type)
        
        if atom_residue in self.NAandWATList:
            return self.get_atom_type(self.NAandWATForceFieldDict,atom_residue, atom_type)

        #Abnormal residue: WAT, LIG, Na+, etc.
        else:
            return self.FFParameter.get(atom_type, 'None')
        
    def get_atom_type(self,ffdict,atom_residue, atom_type):
        residue_dict = ffdict.get(atom_residue, "None")
        if residue_dict == "None":
            return "None"
        else:
            return residue_dict.get(atom_type, "None")