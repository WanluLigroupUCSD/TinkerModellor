from ._water_ions_trans import WaterAndIonsForceField
from .._abc import FroceFieldTrans
from ._gaff import GAFFForceField
from ._amber import AmberForceFieldDict

class AmberGAFFTrans(FroceFieldTrans):
    
    def __init__(self,Aggressive:bool = True):
        """
        Force Field Transformation Dictionary Initialization

        Args:
            Aggressive(bool):   If true, scripts would try to pair more atom types,
                                and this may results mismatching

        Returns:
            
        """
        
        super().__init__()

        #Preparation for the abnormal(water/ions/ligand)force field transformation
        self.aggressive = Aggressive
        self.FFpara = {}
        supported_FFpara = [WaterAndIonsForceField.water_para,WaterAndIonsForceField.ion_para,GAFFForceField.gaff_para]
        
        for i in supported_FFpara:
            self.FFpara.update(i) 
        
        if self.aggressive:
            additional_FFpara = [GAFFForceField.unpair_gaff_para]
            for i in additional_FFpara : self.FFpara.update(i)
        
        #Preparation for the normal(amino acid)force field transformation
        self.force_field_dict = AmberForceFieldDict._amberpara
        self.residue_list =  [
            "ALA", "ARG", "ASN", "ASP", "CYS",
            "GLN", "GLU", "GLY", "HIE", "ILE",
            "LEU", "LYS", "MET", "PHE", "PRO",
            "SER", "THR", "TRP", "TYR", "VAL","HIS"]


    def __call__(self,atom_residue:str, atom_type: str) -> str:
        return self._transform_to_tinker(atom_type,atom_residue)        
    
    def _transform_to_tinker(self, atom_type: str, atom_residue: str) -> str:
    
        #To check whether the residue is normal residue
        #Normal residue: LYS, ARG, GLU, etc.
        if atom_residue in self.residue_list:
            return self.get_atom_type(atom_residue, atom_type)

        #Abnormal residue: WAT, LIG, Na+, etc.
        else:
            return self.FFpara.get(atom_type, 'None')

    def get_atom_type(self,atom_residue, atom_type):
        residue_dict = self.force_field_dict.get((atom_residue), "None")
        if residue_dict == "None":
            return "None"
        else:
            return residue_dict.get((atom_type), "None")