from typing import Any, Tuple
import math
import shlex

from ....build import TinkerSystem
from ._coord_replace import (_coord_replace,_coord_replace_with_ff)
from ._find_coincidence import _find_coincidence
from ._exe_delete_and_move import _exe_delete_and_move

class ReplaceTinkerSystemWithoutFF():
    
    def __init__(self):
        pass

    def __call__(self, tk1:TinkerSystem, tk2:TinkerSystem) -> TinkerSystem:
        """
        This function merges two Tinker systems.
        But the coincident water and ion molecules will be removed.

        Args:
            tk1 (TinkerSystem): The first Tinker system.
            tk2 (TinkerSystem): The second Tinker system.

        Returns:
            TinkerSystem: The merged Tinker system.
        """
        coincidence_list = _find_coincidence(tk1, tk2)
        
        tks_replaced = _coord_replace(tk1, tk2)
        
        tks_replaced = _exe_delete_and_move(tks_replaced, coincidence_list)

        return tks_replaced

class ReplaceTinkerSystemWithFF():
    
    def __init__(self) -> None:
        pass

    def __call__(self, tk1:TinkerSystem, tk2:TinkerSystem,ff1:str, ff2:str, ffout:str=None) -> Tuple[TinkerSystem,str]:
        """
        This function merges two Tinker systems with force field files.
        But the coincident water and ion molecules will be removed.

        Args:
            tk1 (TinkerSystem): The first Tinker system.
            tk2 (TinkerSystem): The second Tinker system.
            ff1 (str): The first force field file.
            ff2 (str): The second force field file.
            ffout (str, optional): The output force field file. Defaults to None.

        Returns:
            Tuple[TinkerSystem,str]: The merged Tinker system and the output force field file.
        """

        # Find the max atom type in the first force field
        atom_type_addition = self._find_max_atom_type(ff1)

        tks_merged = _coord_replace_with_ff(tk1, tk2,atom_type_addition)

        # The atom class and atom type value in the second force field should be adjusted
        # So that two force fields can be merged
        addition_prm = self._process_prm_file(ff2, atom_type_addition)

        with open(ffout, 'w') as file:
            with open(ff1, 'r') as file1:
                file1_lines = file1.readlines()
            file1_lines += addition_prm
            file.writelines(file1_lines)

        return tks_merged, ffout
    
    @staticmethod
    def _find_max_atom_type(ff1:str):
        
        max_value:int = 0

        with open(ff1, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith('atom'):
                parts = line.split()
                max_value = max(max_value, int(parts[1]), int(parts[2]))

        # Round up to the nearest hundred
        rounded_value = math.ceil(max_value / 100.0) * 100
        return rounded_value

    @staticmethod
    def _process_prm_file(file_path, prm_addition_value:int) -> list:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        title = "Force Field Reconstruction by TinkerModellor"
        padding = math.ceil((77 - len(title)) / 2)
        return_line = [
            '\n',
            "#" * 81+'\n',
            "##" + " " * 77 + "##\n",
            "##" + " " * padding + title + " " * (77 - len(title) - padding) + "##\n",
            "##" + " " * 77 + "##\n",
            "#" * 81+'\n',
            '\n'
        ]

        for i, line in enumerate(lines):
            parts = shlex.split(line)
            if line.startswith('atom'):
                parts[1] = str(int(parts[1]) + prm_addition_value)
                parts[2] = str(int(parts[2]) + prm_addition_value)
                parts[4] = "\"Force Field Reconstruction by TinkerModellor\""
            elif line.startswith('vdw'):
                parts[1] = str(int(parts[1]) + prm_addition_value)
            elif line.startswith('bond'):
                parts[1] = str(int(parts[1]) + prm_addition_value)
                parts[2] = str(int(parts[2]) + prm_addition_value)
            elif line.startswith(('angle','ureybrad')):
                parts[1] = str(int(parts[1]) + prm_addition_value)
                parts[2] = str(int(parts[2]) + prm_addition_value)
                parts[3] = str(int(parts[3]) + prm_addition_value)
            elif line.startswith(('torsion', 'improper')):
                parts[1] = str(int(parts[1]) + prm_addition_value)
                parts[2] = str(int(parts[2]) + prm_addition_value)
                parts[3] = str(int(parts[3]) + prm_addition_value)
                parts[4] = str(int(parts[4]) + prm_addition_value)
            elif line.startswith('polarize'):
                parts[1] = str(int(parts[1]) + prm_addition_value)
                if len(parts) >= 5:
                    for j in range(4, len(parts)):
                        parts[j] = str(int(parts[j]) + prm_addition_value)
            elif line.startswith('multipole'):
                if len(parts) == 5:
                    if int(parts[-4]) >= 0:
                        parts[-4] = str(int(parts[-4]) + prm_addition_value)
                    else:
                        parts[-4] = str(int(parts[-4]) - prm_addition_value)
                    if int(parts[-3]) >= 0:
                        parts[-3] = str(int(parts[-3]) + prm_addition_value)
                    else:
                        parts[-3] = str(int(parts[-3]) - prm_addition_value)
                    if int(parts[-2]) >= 0:
                        parts[-2] = str(int(parts[-2]) + prm_addition_value)
                    else:
                        parts[-2] = str(int(parts[-2]) - prm_addition_value)
                elif len(parts) == 4:
                    if int(parts[-3]) >= 0:
                        parts[-3] = str(int(parts[-3]) + prm_addition_value)
                    else:
                        parts[-3] = str(int(parts[-3]) - prm_addition_value)
                    if int(parts[-2]) >= 0:
                        parts[-2] = str(int(parts[-2]) + prm_addition_value)
                    else:
                        parts[-2] = str(int(parts[-2]) - prm_addition_value)
                elif len(parts) == 3:
                    if int(parts[-2]) >= 0:
                        parts[-2] = str(int(parts[-2]) + prm_addition_value)
                    else:
                        parts[-2] = str(int(parts[-2]) - prm_addition_value)        
            elif not any(char.isalpha() for char in line):
                parts = [f"{float(part):.5f}" for part in parts]

            return_line.append(' '.join(parts) + '\n')  
        return return_line    


