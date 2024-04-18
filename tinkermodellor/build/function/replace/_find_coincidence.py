import numpy as np

from ....build import TinkerSystem

MIN_DISTANCE = 1.2

def _find_coincidence(tks1:TinkerSystem, tks2:TinkerSystem):
    """
    This function finds the coincidence of two Tinker systems.

    Args:
        tks1: The first Tinker system.
        tks2: The second Tinker system (which is merged into tks1).

    Returns:
        List[int]: The indices of the atoms in tks1 that are close to any atom in tks2.
    """

    coords1 = tks1.AtomCrds
    coords2 = tks2.AtomCrds

    # Distance calculation
    distances = np.sqrt(((coords1[:, np.newaxis, :] - coords2) ** 2).sum(axis=2))

    # Find the coincidence
    close_indices = np.where(np.any(distances <= MIN_DISTANCE, axis=1))[0]

    close_indices = np.unique(close_indices + 1)  
    close_indices_sorted = np.sort(close_indices)  

    print(close_indices_sorted.tolist())

    return close_indices_sorted.tolist()