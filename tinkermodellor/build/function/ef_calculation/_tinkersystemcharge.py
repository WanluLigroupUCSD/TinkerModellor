import os
import numpy as np

from openbabel import openbabel
from typing import List

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
        self.Charges = []*self.AtomNums
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

    def assign_charge_seperately(self) -> str:

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

    def _connectivity_search(self,ndx: List, bonds) -> List[int]:
        """
        Finds all atoms connected to the initial atom index, ensuring entire molecules or connected components are marked.

        Args:
            initial (int): Initial atom index to start the search.

        Returns:
            List[int]: Complete list of connected atom indices, sorted.
        """

        atom_in_molecule = []
        for initial in ndx:
            # Ensure the initial atom index is valid
            if initial < 1 or initial > len(bonds):
                raise ValueError(f"Initial atom index {initial} is out of bounds.")

            sys.setrecursionlimit(10000)
            residue_list = []
            visited = set()  # Track visited atoms to prevent infinite recursion

            def explore_bonded_atoms(atom_index):
                """Recursively adds bonded atoms to the list."""
                if atom_index in visited:
                    return
                visited.add(atom_index)
                residue_list.append(atom_index)

                for bonded_atom in bonds[atom_index - 1]:  # Adjust for 0-indexing
                    explore_bonded_atoms(bonded_atom)

                

            explore_bonded_atoms(initial)

            # Sort residue_list with the largest number first
            residue_list = sorted(residue_list, reverse=True)

            # Add to atom_in_molecule if not already included
            atom_in_molecule.extend(residue_list)

        # Remove duplicates and sort atom_in_molecule with the largest number first
        atom_in_molecule = sorted(set(atom_in_molecule), reverse=True)

        return atom_in_molecule

if __name__ == '__main__':
    charge = TinkerSystemCharge()
    charge.read_tinker_xyz('./example/merge/ex1/ligand.xyz')
