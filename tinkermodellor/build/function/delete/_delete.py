from typing import List,Union

import numpy as np

from ...system.tinker._tinkersystem import TinkerSystem
from ...function.merge._reset import _reset

from ....messager import TKMDeleteReminder

class DeleteTinkerSystem():

    def __init__(self):
        pass

    @TKMDeleteReminder
    def __call__(self,tks:TinkerSystem, index:Union[int,List[int],List[str],str]) -> TinkerSystem:
        """
        This function deletes atoms from a Tinker system.

        Args:
            tks (TinkerSystem): The Tinker system.
            index (List[int]): The index of the atoms to be deleted.

        Returns:
            TinkerSystem: The Tinker system after deletion.
        """

        if isinstance(index, int):
            index = [index]
        elif isinstance(index, str):
            index = [int(index)]
        elif isinstance(index, list):
            if isinstance(index[0], str):
                index = [int(i) for i in index]
        else:
            raise ValueError("The index should be int, str or list.")
        
        # Creation a index list without duplication
        index = list(set(index))

        ### It is REALLY IMPORTANT to sort the index in reverse order ###
        ### Otherwise, the index will be wrong after the first deletion ###
        ### For example, if we delete the first atom, the second atom will be the first one ###
        ### Then if we delete the second atom in original order, the third atom (original) will be deleted ###
        index = sorted(index, reverse=True)

        for ndx_iter in index:
            if ndx_iter <= 0 or ndx_iter > tks.AtomNums:
                raise ValueError("Index out of range.")
            
            else:
                print("Deleting an atom with index of %d" % ndx_iter)
                print('Updating the connectivity...\n')
                # The index in tks is from 0 to AtomNums
                tks_index = ndx_iter -1

                # Delete the atom line directly
                self._delete(tks,tks_index)

                # Update connectivity
                self._update_connectivity(tks,tks_index)

                # Update the connectivity
                tks.check()

        return tks
        

        
    def _delete(self,tks:TinkerSystem, tks_index:int) -> TinkerSystem:

        # Delete the corresponding elementks from the properties
        del tks.AtomTypesStr[tks_index]
        del tks.Bonds[tks_index]

        tks.AtomCrds = np.delete(tks.AtomCrds,tks_index, axis=0)
        tks.AtomTypesNum = np.delete(tks.AtomTypesNum,tks_index)

        
        # Update AtomIndex
        tks.AtomNums -= 1
        tks.AtomIndex = np.arange(1, len(tks.AtomCrds))
        
        

    def _update_connectivity(self,tks:TinkerSystem, tks_index:int) -> TinkerSystem:

        for i in range(len(tks.Bonds)):
            tks.Bonds[i] = [bond for bond in tks.Bonds[i] if bond != tks_index+1]

        # Update the connectivity
        for i in range(len(tks.Bonds)):
            tks.Bonds[i] = [bond-1 if bond > tks_index+1 else bond for bond in tks.Bonds[i]]