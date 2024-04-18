from ._replace_class import ReplaceTinkerSystemWithoutFF
from ._replace_class import ReplaceTinkerSystemWithFF
from ....build import TinkerSystem

from ....messager import TKMMergeReminder

class ReplaceTinkerSystem():
    def __init__(self) -> None:
        pass

    @TKMMergeReminder
    def __call__(self, tk1:TinkerSystem, tk2:TinkerSystem,ff1:str=None, ff2:str=None, ffout:str=None) -> TinkerSystem:
        
        """
        This function merges two Tinker systems with force field files.

        Args:
            tk1 (TinkerSystem): The first Tinker system.
            tk2 (TinkerSystem): The second Tinker system.
            ff1 (str): The first force field file (optional).
            ff2 (str): The second force field file (optional, when ff1 is required this should also be required).
            ffout (str, optional): The output force field file (optional). Defaults to None.

        Returns:
            TinkerSystem: The merged Tinker system and the output force field file.
        """
            
        if ff1 is None and ff2 is None and ffout is None:
            merge = ReplaceTinkerSystemWithoutFF()
            tks_replaced = merge(tk1, tk2)
            
        else:
            if ff1 is not None and ff2 is not None and ffout is not None:
                merge = ReplaceTinkerSystemWithFF()

                tks_replaced, ffout = merge(tk1, tk2, ff1, ff2, ffout)
                print('Output Force Field File:', ffout)
            else:
                raise ValueError('Please provide the force field files (ff1 and ff2) and the output force field file (ffout)')
            
        tks_replaced.check()
        
        return tks_replaced
