from ....build import TinkerSystem
import numpy as np
from typing import Tuple

def _coord_merge(tk1:TinkerSystem, tk2:TinkerSystem) -> TinkerSystem:

    tkm_merged = tk1

    # Define the box size and box angle of the merged system    
    if tk1.BoxSize is None and tk2.BoxSize is None:
        print('WARNING!!! No box size found in the two systems')
    elif tk1.BoxSize is None and tk2.BoxSize is not None:
        print('WARNING!!! The box size of the first system is not found, the box size of the second system will be used')
        tkm_merged.BoxSize = tk2.BoxSize
    elif np.array_equal(tk1.BoxSize, tk2.BoxSize):
        print('WARNING!!! The box size of the two systems are different, the box size of the first system will be used')

    if tk1.BoxAngle is None and tk2.BoxAngle is None:
        print('WARNING!!! No box angle found in the two systems')
    elif tk1.BoxAngle is None and tk2.BoxAngle is not None:
        print('WARNING!!! The box angle of the first system is not found, the box angle of the second system will be used')
        tkm_merged.BoxAngle = tk2.BoxAngle
    elif np.array_equal(tk1.BoxAngle, tk2.BoxAngle):
        print('WARNING!!! The box angle of the two systems are different, the box angle of the first system will be used')


    index1 = tk1.AtomNums

    tkm_merged.AtomNums += tk2.AtomNums

    # Simple merge of the two systems
    tkm_merged.AtomTypesStr.extend(tk2.AtomTypesStr)
    tkm_merged.AtomCrds = np.concatenate((tkm_merged.AtomCrds, tk2.AtomCrds))
    tkm_merged.AtomTypesNum = np.concatenate((tkm_merged.AtomTypesNum, tk2.AtomTypesNum))

    # For connectivity and Atom Index should be adjusted
    tk2_bonds_adjusted = []    
    for bond in tk2.Bonds:
        bond_list = [element + index1 for element in bond]
        tk2_bonds_adjusted.append(bond_list)
    tkm_merged.Bonds.extend(tk2_bonds_adjusted)

    # Index just is regenerated for the new system
    tkm_merged.AtomIndex = np.arange(1, tkm_merged.AtomNums)

    # Check the merged system
    tkm_merged.check()

    return tkm_merged

def _coord_merge_with_ff(tk1:TinkerSystem, tk2:TinkerSystem, atom_type_addition:int) -> TinkerSystem:

    tkm_merged = tk1

    # Define the box size and box angle of the merged system    
    if tk1.BoxSize is None and tk2.BoxSize is None:
        print('WARNING!!! No box size found in the two systems')
    elif tk1.BoxSize is None and tk2.BoxSize is not None:
        print('WARNING!!! The box size of the first system is not found, the box size of the second system will be used')
        tkm_merged.BoxSize = tk2.BoxSize
    elif np.array_equal(tk1.BoxSize, tk2.BoxSize):
        print('WARNING!!! The box size of the two systems are different, the box size of the first system will be used')

    if tk1.BoxAngle is None and tk2.BoxAngle is None:
        print('WARNING!!! No box angle found in the two systems')
    elif tk1.BoxAngle is None and tk2.BoxAngle is not None:
        print('WARNING!!! The box angle of the first system is not found, the box angle of the second system will be used')
        tkm_merged.BoxAngle = tk2.BoxAngle
    elif np.array_equal(tk1.BoxAngle, tk2.BoxAngle):
        print('WARNING!!! The box angle of the two systems are different, the box angle of the first system will be used')


    index1 = tk1.AtomNums

    tkm_merged.AtomNums += tk2.AtomNums

    # Simple merge of the two systems
    tkm_merged.AtomTypesStr.extend(tk2.AtomTypesStr)
    tkm_merged.AtomCrds = np.concatenate((tkm_merged.AtomCrds, tk2.AtomCrds))
    tkm_merged.AtomTypesNum = np.concatenate((tkm_merged.AtomTypesNum, tk2.AtomTypesNum+atom_type_addition))

    # For connectivity and Atom Index should be adjusted
    tk2_bonds_adjusted = []    
    for bond in tk2.Bonds:
        bond_list = [element + index1 for element in bond]
        tk2_bonds_adjusted.append(bond_list)
    tkm_merged.Bonds.extend(tk2_bonds_adjusted)

    # Index just is regenerated for the new system
    tkm_merged.AtomIndex = np.arange(1, tkm_merged.AtomNums)

    # Check the merged system
    tkm_merged.check()

    return tkm_merged