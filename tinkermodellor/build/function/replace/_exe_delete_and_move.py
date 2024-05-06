from typing import List

from ....build import TinkerSystem
from ....build import DeleteTinkerSystem
from ._connectivity_search import _connectivity_search

def _exe_delete_and_move(tks1:TinkerSystem, delete_list:List) -> TinkerSystem:
    """
    This function deletes the coincident water and ion molecules in tks1
    And moves the coincident atom in other molecule to a proper coordination in tks2 to tks1.

    Args:
        tks1 (DeleteTinkerSystem): The first Tinker system.

    Returns:
        DeleteTinkerSystem: The merged Tinker system.
    """

    added_delete_list = _connectivity_search(tks1, delete_list)
    
    print('Completed Delete list:',added_delete_list)

    delete = DeleteTinkerSystem()

    # If no atom is found to be deleted, raise an error

    if added_delete_list == []:
        raise ValueError("No atom is found to be deleted. The Replace function is not necessary. Maybe you should use the Merge function.")
    delete(tks1, added_delete_list)

    return tks1