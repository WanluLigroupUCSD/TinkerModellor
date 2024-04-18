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
    expanded_delete_set = set(initial_delete_list)  # 使用集合避免重复
    visited = set()  # 追踪已访问的原子

    def explore_bonded_atoms(atom_index):
        """ Recursively adds bonded atoms to the delete set. """
        if atom_index in visited:
            return
        visited.add(atom_index)
        expanded_delete_set.add(atom_index)
        for bonded_atom in tks.Bonds[atom_index - 1]:  # Adjust for 0-indexing
            explore_bonded_atoms(bonded_atom)

    for index in initial_delete_list:
        explore_bonded_atoms(index)

    return sorted(expanded_delete_set)