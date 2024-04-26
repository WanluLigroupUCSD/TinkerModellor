import os
from typing import List, Union

from tinkermodellor.build import TinkerSystem
from tinkermodellor.build import GMXSystem
from tinkermodellor.build import Transformer

from tinkermodellor.build import MergeTinkerSystem
from tinkermodellor.build import DeleteTinkerSystem
from tinkermodellor.build import ReplaceTinkerSystem

from tinkermodellor.build import TKMTrajectory

import tinkermodellor.tkmtoolkit as ttk

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

    def replace(self,tk1:str,tk2:str, tinker_xyz:str=None, ff1:str=None, ff2:str=None, ffout:str=None) -> TinkerSystem:
        """
        This function merges two Tinker systems with or without force field files.
        But coincident water and ion molecules in tk1 would be deleted.

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

        replace = ReplaceTinkerSystem()
        tks_replaced = replace(tks1, tks2, ff1, ff2, ffout)

        if tinker_xyz is not None:
            tks_replaced.write(tinker_xyz)

        return tks_replaced
    
    def rmsd(self, xyz:str, arc:str, ref:str = None, skip:int = None) -> List[float]:
        """
            Calculate the RMSD of Tinker trajectories.
        
        Args:
            xyz (str): Path to the xyz file.
            arc (str): Path to the arc file.
            ref (str, optional): Path to the reference xyz file. Defaults to None.
            skip (int, optional): Skip frames. Defaults to None.
        
        Returns:
            List: A list of RMSD values.
        """

        if isinstance(xyz, str):
            xyz = os.path.abspath(xyz)
        else:
            raise TypeError("The xyz file path must be a string.")
        
        if isinstance(arc, str):
            arc = os.path.abspath(arc)
        else:
            raise TypeError("The arc file path must be a string.")
        
        input = TKMTrajectory()
        input.read_from_tinker(xyz)
        input.read_from_traj(arc)


        if skip is None:
            traj = input.AtomCrds
        else:
            traj = input.AtomCrds[::skip]
            print(f"Skipping every {skip} frames. Total frames: {len(traj)}.")

        if ref is not None:
            ref = TKMTrajectory()
            ref.read_from_tinker(ref)
            ref_traj = ref.AtomCrds[0]
        else:
            ref_traj = traj[0]

        output = ttk.rmsd(ref_traj, traj)
        output = [round(float(i), 6) for i in output]
        return output


if __name__ == '__main__':
    control = 6
    tkm= TinkerModellor()

    # Transform
    if control == 0:
        tkm.transform(r'/home/wayne/quanmol/TinkerModellor/example/gmx_format/gromacs.gro',r'/home/wayne/quanmol/TinkerModellor/example/gmx_format/gromacs.top')

    # Merge
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
        
    # Delete
    elif control ==3 :
        tkm.delete(tk =r'/home/wayne/quanmol/TinkerModellor/example/delete/ex2/ligand.xyz',\
                   tinker_xyz=r'/home/wayne/quanmol/TinkerModellor/example/delete/ex2/deleted.xyz',\
                    index=[1,6,30])
        
    # Replace
    elif control ==4:
        tkm.replace(tk1=r'/home/wayne/quanmol/TinkerModellor/example/replace/ex1/protein.xyz',\
                  tk2=r'/home/wayne/quanmol/TinkerModellor/example/replace/ex1/ligand.xyz',\
                  tinker_xyz=r'/home/wayne/quanmol/TinkerModellor/example/replace/ex1/replaced_with_ff.xyz',\
                  ff1=r'/home/wayne/quanmol/TinkerModellor/example/replace/ex1/amoebabio18.prm',\
                  ff2=r'/home/wayne/quanmol/TinkerModellor/example/replace/ex1/ligand.prm',\
                  ffout=r'/home/wayne/quanmol/TinkerModellor/example/replace/ex1/replaced_with_ff.prm')
    elif control ==5:
        tkm.replace(tk1=r'/home/wayne/quanmol/TinkerModellor/example/replace/ex1/protein.xyz',\
                  tk2=r'//home/wayne/quanmol/TinkerModellor/example/replace/ex1/ligand.xyz',\
                  tinker_xyz=r'/home/wayne/quanmol/TinkerModellor/example/replace/ex1/replaced_withoud_ff.xyz',)
    elif control == 6:
        output = tkm.rmsd(xyz=r'/home/wayne/quanmol/TinkerModellor/example/rmsd/pr_coord.xyz',\
                        arc = r'/home/wayne/quanmol/TinkerModellor/example/rmsd/pr_coord.arc',
                        skip=10)
        print(output)