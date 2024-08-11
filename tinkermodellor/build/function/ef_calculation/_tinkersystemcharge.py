import os
import numpy as np

from openbabel import openbabel

#from tinkermodellor import TinkerSystem
from ...system.tinker._tinkersystem import TinkerSystem


class TinkerSystemCharge(TinkerSystem):
    def __init__(self, charge_method: str = None):
        super().__init__()
        self.Charges: np.array

        if charge_method is None:
            print("No charge method specified, using default charge method: eem")
            self.charge_method = 'eem'
        elif charge_method not in ['eem', 'qeq', 'qtpie']:
            raise NotImplementedError(f"Charge method {charge_method} not implemented")
        else:
            self.charge_method = charge_method

    def __call__(self, input: str = None):
        path = os.path.abspath(input)
        self.read_from_tinker(path)
        self.assign_charge()
        return self

    def read_tinker_xyz(self, tinker_xyz: str):
        self.read_from_tinker(tinker_xyz)

    def assign_charge(self) -> str:

        print(f"Assigning charges using {self.charge_method} method\nThis may take a while...")
        def str2num(atom_type):

            if len(atom_type) == 1:
                atom_type_modify = atom_type
            elif atom_type[1].islower():
                atom_type_modify = atom_type[0:2]
            else:
                atom_type_modify = atom_type[0]

            element_dict = {
                'H': 1, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 
                'P': 15, 'S': 16, 'Cl': 17, 'Br': 35, 'Fe': 26,
            }
            return element_dict.get(atom_type_modify, 0)
            
        obConversion = openbabel.OBConversion()
        obConversion.SetOutFormat('sdf')

        mol = openbabel.OBMol()

        # Add atoms
        for i in range(len(self.AtomTypesStr)):
            atom = mol.NewAtom()
            atom.SetAtomicNum(str2num(self.AtomTypesStr[i]))
            atom.SetVector(self.AtomCrds[i][0], self.AtomCrds[i][1], self.AtomCrds[i][2])

        # Add bonds
        for i in range(len(self.Bonds)):
            for bond_num in self.Bonds[i]:
                mol.AddBond(i + 1, bond_num, 1)

        mol.PerceiveBondOrders()

        mol.SetTitle(self.SystemName)

        # Compute charges
        chargeModel = openbabel.OBChargeModel.FindType(self.charge_method)
        chargeModel.ComputeCharges(mol)

        # Assign charges to self.charges
        self.Charges = np.array([atom.GetPartialCharge() for atom in openbabel.OBMolAtomIter(mol)])


if __name__ == '__main__':
    charge = TinkerSystemCharge()
    charge.read_tinker_xyz('./example/merge/ex1/ligand.xyz')
