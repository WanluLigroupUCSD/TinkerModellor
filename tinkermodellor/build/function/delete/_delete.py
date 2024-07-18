from typing import List,Union

import numpy as np

from ...system.tinker._tinkersystem import TinkerSystem
from ...function.merge._reset import _reset

from ....messager import TKMDeleteReminder

class DeleteTinkerSystem():

    def __init__(self):
        pass

    @TKMDeleteReminder
    def __call__(self,tks:TinkerSystem, IndexToBeDel:Union[int,List[int],List[str],str]) -> TinkerSystem:
        """
        This function deletes atoms from a Tinker system.

        Args:
            tks (TinkerSystem): The Tinker system.
            index (List[int]): The index of the atoms to be deleted.

        Returns:
            TinkerSystem: The Tinker system after deletion.
        """

        if isinstance(IndexToBeDel, int):
            IndexToBeDel = [IndexToBeDel]
        elif isinstance(IndexToBeDel, str):
            IndexToBeDel = [int(IndexToBeDel)]
        elif isinstance(IndexToBeDel, list):
            if isinstance(IndexToBeDel[0], str):
                IndexToBeDel = [int(i) for i in IndexToBeDel]
        else:
            raise ValueError("The index should be int, str or list.")
        
        # Creation a index list without duplication
        IndexToBeDel = list(set(IndexToBeDel))

        ### It is REALLY IMPORTANT to sort the index in reverse order ###
        ### Otherwise, the index will be wrong after the first deletion ###
        ### For example, if we delete the first atom, the second atom will be the first one ###
        ### Then if we delete the second atom in original order, the third atom (original) will be deleted ###
        IndexToBeDel = sorted(IndexToBeDel, reverse=True)

        count = 0
        for ndx_iter in IndexToBeDel:
            if ndx_iter <= 0 or ndx_iter > tks.AtomNums:
                raise ValueError(f"Index {ndx_iter} out of range [{1}, {tks.AtomNums}].")
            
            else:
                print("Deleting an atom with index of %d" % ndx_iter, f'and its atom type is {tks.AtomTypesStr[ndx_iter-1]}')
                print('Updating the connectivity...\n')
                # The index in tks is from 0 to AtomNums
                tks_index = ndx_iter -1

                # Delete the atom line directly
                self._delete(tks,tks_index)

                # Update connectivity
                self._update_connectivity(tks,tks_index)

                # Check the connectivity
                tks.check()
                count +=1
                
        print(f'{count} atoms have been deleted.')

        return tks
        

        
    def _delete(self,tks:TinkerSystem, tks_index:int):

        # Delete the corresponding elementks from the properties
        del tks.AtomTypesStr[tks_index]
        del tks.Bonds[tks_index]

        tks.AtomCrds = np.delete(tks.AtomCrds,tks_index, axis=0)
        tks.AtomTypesNum = np.delete(tks.AtomTypesNum,tks_index)

        
        # Update AtomIndex
        tks.AtomNums -= 1
        tks.AtomIndex = np.arange(1, len(tks.AtomCrds)+1)
        
        

    def _update_connectivity(self,tks:TinkerSystem, tks_index:int):

        for i in range(len(tks.Bonds)):
            tks.Bonds[i] = [bond for bond in tks.Bonds[i] if bond != tks_index+1]

        # Update the connectivity
        for i in range(len(tks.Bonds)):
            tks.Bonds[i] = [bond-1 if bond > tks_index+1 else bond for bond in tks.Bonds[i]]