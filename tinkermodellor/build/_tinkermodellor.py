import os
from typing import List, Union

from tinkermodellor.build import TinkerSystem
from tinkermodellor.build import GMXSystem
from tinkermodellor.build import Transformer

from tinkermodellor.build import MergeTinkerSystem
from tinkermodellor.build import DeleteTinkerSystem

class TinkerModellor:

    def __init__(self) -> None:
        pass

    def transform(self,gmx_gro:str,gmx_top:str,tinker_xyz:str =None) -> TinkerSystem:
        """
        Transform a Gromacs system to a Tinker system.
        If tinker_xyz is given, the Tinker system will be written to the file.

        Args:
            gmx_gro (str): Path to the Gromacs .gro file.
            gmx_top (str): Path to the Gromacs .top file.
            tinker_xyz (str, optional): Path to the Tinker .xyz file. Defaults to None.
        
        Returns:
            TinkerSystem: The Tinker system.

        Usage:
            tkm= TinkerModellor()
            tinker_system = tkm(r'/path/to/your/gromacs.gro',r'/path/to/your/gromacs.top')
        """


        gmx_gro = os.path.abspath(gmx_gro)
        gmx_top = os.path.abspath(gmx_top)

        if tinker_xyz is not None:
            tinker_xyz = os.path.abspath(tinker_xyz)

        gmx = GMXSystem()
        gmx.read_gmx_file(gmx_gro, gmx_top)
        transformer = Transformer()
        tk = transformer(gmx)

        if tinker_xyz is not None:
            tk.write(tinker_xyz)

        return tk
    
    def merge(self,tk1:str,tk2:str, tinker_xyz:str=None, ff1:str=None, ff2:str=None, ffout:str=None) -> TinkerSystem:
        """
        This function merges two Tinker systems with or without force field files.

        Args:
            tk1 (TinkerSystem): The first Tinker system.
            tk2 (TinkerSystem): The second Tinker system.
            ff1 (str): The first force field file (optional).
            ff2 (str): The second force field file (optional, when ff1 is required this should also be required).
            ffout (str, optional): The output force field file (optional). Defaults to None.

        Returns:
            TinkerSystem: The merged Tinker system and the output force field file.
        """

        tk1 = os.path.abspath(tk1)
        tk2 = os.path.abspath(tk2)
        if tinker_xyz is not None:
            tinker_xyz = os.path.abspath(tinker_xyz)
        if ff1 is not None:
            ff1 = os.path.abspath(ff1)
        if ff2 is not None:
            ff2 = os.path.abspath(ff2)
        if ffout is not None:
            ffout = os.path.abspath(ffout)
        
        tks1 = TinkerSystem()
        tks1.read_from_tinker(tk1)
        tks2 = TinkerSystem()
        tks2.read_from_tinker(tk2)

        merge = MergeTinkerSystem()
        tks_merged = merge(tks1, tks2, ff1, ff2, ffout)

        if tinker_xyz is not None:
            tks_merged.write(tinker_xyz)

        return tks_merged
    
    def delete(self,tk:str, index:Union[int,List[int],List[str],str],tinker_xyz:str=None,) -> TinkerSystem:
        """
        Delete atoms in the Tinker system.

        Args:
            tk (str): Path to the Tinker system.
            tinker_xyz (str): Path to the output Tinker system.
            index (Union[int,List[int],List[str],str]): The index of the atoms to be deleted.

        Returns:
            TinkerSystem: The Tinker system after deletion.
        """

        tk = os.path.abspath(tk)
        tinker_xyz = os.path.abspath(tinker_xyz)

        dele = DeleteTinkerSystem()
        tks = TinkerSystem()

        tks.read_from_tinker(tk)
        tks_deleted = dele(tks,index)

        if tinker_xyz is not None:
            tks_deleted.write(tinker_xyz)
         
        return tks_deleted



if __name__ == '__main__':
    control = 3
    tkm= TinkerModellor()
    if control == 0:
        tkm.transform(r'/home/wayne/quanmol/TinkerModellor/example/gmx_format/gromacs.gro',r'/home/wayne/quanmol/TinkerModellor/example/gmx_format/gromacs.top')
    elif control ==1:
        tkm.merge(tk1=r'/home/wayne/quanmol/TinkerModellor/example/test/test.xyz',\
                  tk2=r'/home/wayne/quanmol/TinkerModellor/example/test/test.xyz',\
                  tinker_xyz=r'/home/wayne/quanmol/TinkerModellor/example/test/merged.xyz',)
    elif control ==2:
        tkm.merge(tk1=r'/home/wayne/quanmol/TinkerModellor/example/tinker_format/merge_case/protein.xyz',\
                  tk2=r'/home/wayne/quanmol/TinkerModellor/example/tinker_format/merge_case/ligand.xyz',\
                  tinker_xyz=r'/home/wayne/quanmol/TinkerModellor/example/tinker_format/merge_case/merged.xyz',\
                  ff1=r'/home/wayne/quanmol/TinkerModellor/example/tinker_format/merge_case/amoebabio18.prm',\
                  ff2=r'/home/wayne/quanmol/TinkerModellor/example/tinker_format/merge_case/ligand.prm',\
                  ffout=r'/home/wayne/quanmol/TinkerModellor/example/tinker_format/merge_case/merged.prm')
    elif control ==3 :
        tkm.delete(tk =r'/home/wayne/quanmol/TinkerModellor/example/delete/ex2/ligand.xyz',\
                   tinker_xyz=r'/home/wayne/quanmol/TinkerModellor/example/delete/ex2/deleted.xyz',\
                    index=[1,6,30])
    
