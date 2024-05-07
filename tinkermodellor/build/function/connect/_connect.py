from typing import List,Union

import numpy as np

from ...system.tinker._tinkersystem import TinkerSystem

from ....messager import TKMConnectReminder

class ConnectTinkerSystem():

    def __init__(self):
        pass

    @TKMConnectReminder
    def __call__(self,tks:TinkerSystem, index:Union[int,List[int],List[str],str]) -> TinkerSystem:
        """
        This function connects atoms in a Tinker system.

        Args:
            tks (TinkerSystem): The Tinker system.
            index (List[int]): The index of the atoms to be deleted.

        Returns:
            TinkerSystem: The Tinker system after connection.
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
        
        index = list(set(index))
        if len(index) != 2:
            raise ValueError("The index should be a list with two elements.")


        tks.Bonds[index[0]].append(index[1]) 
        tks.Bonds[index[1]].append(index[0])

        return tks