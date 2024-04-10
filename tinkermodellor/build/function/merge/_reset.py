import numpy as np
from ....build import TinkerSystem

def _reset(tks:TinkerSystem) -> TinkerSystem:

    index_initial = tks.AtomIndex[0] -1
    
    # For connectivity and Atom Index should be adjusted
    tks_bonds_adjusted = []    
    for bond in tks.Bonds:
        bond_list = [element - index_initial for element in bond]
        tks_bonds_adjusted.append(bond_list)
    tks.Bonds = tks_bonds_adjusted

    # Index just is regenerated for the new system
    tks.AtomIndex = np.arange(1, tks.AtomNums)

    if not isinstance(tks.AtomTypesNum, np.ndarray):
        tks.AtomTypesNum = np.array(tks.AtomTypesNum)
    # Check the merged system
    tks.check()

    return tks