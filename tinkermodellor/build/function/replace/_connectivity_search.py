from typing import List
from ....build import TinkerSystem

def _connectivity_search(tks: TinkerSystem, initial_delete_list: List[int]) -> List[int]:
    """
    Extends the deletion list to include all atoms connected to any atom already listed for deletion,
    ensuring entire molecules or connected components are marked for deletion.

    Args:
        tks (TinkerSystem): The Tinker system.
        initial_delete_list (List[int]): Initial list of atom indices marked for deletion.

    Returns:
        List[int]: Complete list of atom indices to delete, including all connected atoms.
    """
    WATER_AND_IONS = [350, 349, 363, 352]  # Water and ion atom types

    expanded_delete_set = set()
    non_water_ion_delete_set = set()

    visited = set()  # Track visited atoms to prevent infinite recursion

    def explore_bonded_atoms(atom_index):
        """ Recursively adds bonded atoms to the delete set. """
        if atom_index in visited:
            return
        visited.add(atom_index)
        if tks.AtomTypesNum[atom_index - 1] in WATER_AND_IONS :
            expanded_delete_set.add(atom_index)
            for bonded_atom in tks.Bonds[atom_index - 1]:  # Adjust for 0-indexing
                explore_bonded_atoms(bonded_atom)
        else:
            non_water_ion_delete_set.add(atom_index)

    for index in initial_delete_list:
        if index in visited:  # If already visited, skip to prevent redundant checks
            continue
        explore_bonded_atoms(index)

    # Convert sets to sorted lists before returning
    return sorted(expanded_delete_set)