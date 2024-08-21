import os
from typing import List, Union, Tuple

import numpy as np

from tinkermodellor.build import TinkerSystem
from tinkermodellor.build import TinkerSystemCharge

from tinkermodellor.build import GMXSystem
from tinkermodellor.build import Transformer


from tinkermodellor.build import MergeTinkerSystem
from tinkermodellor.build import DeleteTinkerSystem
from tinkermodellor.build import ReplaceTinkerSystem
from tinkermodellor.build import ConnectTinkerSystem
from tinkermodellor.build import Tinker2PDB
from tinkermodellor.build import ElectricFieldCompute
from tinkermodellor.build import ElectricFieldComputeTraj

from tinkermodellor.build import TKMTrajectory

import tinkermodellor.tkmtoolkit as ttk


class TinkerModellor:

    def __init__(self) -> None:
        pass

    def transform(self,gmx_gro:str,gmx_top:str,tinker_xyz:str =None, forcefield:int =1) -> TinkerSystem:
        """
        Transform a Gromacs system to a Tinker system.
        If tinker_xyz is given, the Tinker system will be written to the file.

        Args:
            gmx_gro (str): Path to the Gromacs .gro file.
            gmx_top (str): Path to the Gromacs .top file.
            tinker_xyz (str, optional): Path to the Tinker .xyz file. Defaults to None.
            forcefield (int, optional): The force field to be used. Defaults to 1.\
            1: AMOEBABIO18, 2: AMOEBABIO09, 3: AMOEBAPRO13

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
        transformer = Transformer(forcefield=forcefield)
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
            ff2 (str): The second force field file (optional, when ff1 is provided this should also be required).
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
    
    def rmsd(self, xyz:str, arc:str, ref:str = None, skip:int = None, ndx:List[int] = None,
            bfra:int = 0, efra:int = -1) -> List[float]:
        """
            Calculate the RMSD of Tinker trajectories.
        
        Args:
            xyz (str): Path to the xyz file.
            arc (str): Path to the arc file.
            ref (str, optional): Path to the reference xyz file. Defaults to None.
            skip (int, optional): Skip frames. Defaults to None.
            ndx (List[int], optional): Index of the atoms. Defaults to None.
            bfra (int, optional): The beginning frame. Defaults to 0.
            efra (int, optional): The ending frame. Defaults to -1.
        
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

        traj = input.AtomCrds

        if skip is not None:
            print(f"Skipping every {skip} frames. Total frames: {len(traj)}.")
            traj = input.AtomCrds[::skip]

        if ref is not None:
            ref = TKMTrajectory()
            ref.read_from_tinker(ref)
            ref_traj = ref.AtomCrds[0]
        else:
            ref_traj = traj[0]

        if ndx is not None:
            # Convert the index to 0-based
            # The index in the trajectory file is 1-based
            ndx = [elemnt-1 for elemnt in ndx]

            traj = traj[:, ndx]
            ref_traj = ref_traj[ndx]
        else:
            pass

            ref_copy = np.copy(ref_traj)
            traj_copy = np.copy(traj[bfra:efra])

        output = ttk.rmsd(ref_copy, traj_copy)
        output = [round(float(i), 6) for i in output]
        return output
    
    def distance(self, xyz:str, arc:str, skip:int = None, ndx:List[int] = None,
            bfra:int = 0, efra:int = -1) -> Tuple[List[float], float]:
        """
            Calculate the distance of Tinker trajectories.
        
        Args:
            xyz (str): Path to the xyz file.
            arc (str): Path to the arc file.
            skip (int, optional): Skip frames. Defaults to None.
            ndx (List[int]): Index of the atoms. Defaults to None.
            bfra (int, optional): The beginning frame. Defaults to 0.
            efra (int, optional): The ending frame. Defaults to -1.
        
        Returns:
            Tuple: A tuple of the distance values and the average distance.
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

        traj = input.AtomCrds

        if skip is not None:
            print(f"Skipping every {skip} frames. Total frames: {len(traj)}.")
            traj = input.AtomCrds[::skip]
            

        if len(ndx) != 2:
            raise ValueError("The index must contain two elements.")
        else:
            # Convert the index to 0-based
            # The index in the trajectory file is 1-based
            ndx = [elemnt-1 for elemnt in ndx]

            atom1_traj = traj[:, ndx[0]]
            atom2_traj = traj[:, ndx[1]]

            atom1_copy = np.copy(atom1_traj[bfra:efra])
            atom2_copy = np.copy(atom2_traj[bfra:efra])

        output = ttk.distance(atom1_copy, atom2_copy)
        output = [round(float(i), 6) for i in output]

        avg_output = sum(output)/len(output)
        print(f"The average distance is {avg_output}.")
        return output, avg_output
    
    def angle(self, xyz:str, arc:str, skip:int = None, ndx:List[int] = None,
            bfra:int = 0, efra:int = -1) -> Tuple[List[float], float]:
        """
            Calculate the atomic angle of Tinker trajectories.
        
        Args:
            xyz (str): Path to the xyz file.
            arc (str): Path to the arc file.
            skip (int, optional): Skip frames. Defaults to None.
            ndx (List[int]): Index of the atoms. Defaults to None.
            bfra (int, optional): The beginning frame. Defaults to 0.
            efra (int, optional): The ending frame. Defaults to -1.
        
        Returns:
            Tuple: A tuple of the distance values and the average distance.
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

        traj = input.AtomCrds

        if skip is not None:
            print(f"Skipping every {skip} frames. Total frames: {len(traj)}.")
            traj = input.AtomCrds[::skip]

        if len(ndx) != 3:
            raise ValueError("The index must contain three elements.")
        else:
            # Convert the index to 0-based
            # The index in the trajectory file is 1-based
            ndx = [elemnt-1 for elemnt in ndx]

            atom1_traj = traj[:, ndx[0],:]
            atom2_traj = traj[:, ndx[1],:]
            atom3_traj = traj[:, ndx[2],:]

            atom1_copy = np.copy(atom1_traj[bfra:efra])
            atom2_copy = np.copy(atom2_traj[bfra:efra])
            atom3_copy = np.copy(atom3_traj[bfra:efra])

        output = ttk.angle(atom1_copy, atom2_copy,atom3_copy)
        output = [round(float(i), 6) for i in output]

        avg_output = sum(output)/len(output)
        print(f"The average distance is {avg_output}.")
        return output, avg_output
    
    def connect(self,tk:str, index:Union[int,List[int],List[str],str],tinker_xyz:str=None,) -> TinkerSystem:
        """
        Connect atoms in the Tinker system.

        Args:
            tk (str): Path to the Tinker system.
            tinker_xyz (str): Path to the output Tinker system.
            index (Union[int,List[int],List[str],str]): The index of the atoms to be connected.

        Returns:
            TinkerSystem: The Tinker system after connection.
        """

        tk = os.path.abspath(tk)
        tinker_xyz = os.path.abspath(tinker_xyz)

        conn = ConnectTinkerSystem()
        tks = TinkerSystem()

        tks.read_from_tinker(tk)
        tks_connected = conn(tks,index)

        if tinker_xyz is not None:
            tks_connected.write(tinker_xyz)
         
        return tks_connected
    
    def tk2pdb(self,tk:str,pdb:str, depth:int=10000, style:int=1) -> str:
        """
        Convert a Tinker system to a PDB file.

        Args:
            tk (str): Path to the Tinker system.
            pdb (str): Path to the output PDB file.
            depth (int, optional): The depth of the searching algorithm.
            style (int, optional): The style of the XYZ file. Defaults to 1.

        Returns:
            str: The PDB file.

        Usage:
            tkm= TinkerModellor()
            tkm.tk2pdb(r'/path/to/your/tinker.xyz',r'/path/to/your/output.pdb')
        """

        tk = os.path.abspath(tk)
        pdb = os.path.abspath(pdb)

        tkpdb = Tinker2PDB(depth)
        tkpdb(tk, pdb, style)

        return tkpdb

    def electric_field_point(self, point: Union[List, np.ndarray], charge_method: str = 'eem', 
                            tinker_xyz: str = None) -> List[float]:
        """
        Compute the electric field at the specified points.

        Args:
            point (Union[List,np.ndarray]): The points where the electric field is computed.
            charge_method (str, optional): The charge method. Defaults to 'eem'. (eem, qeq, qtpie)
            tinker_xyz (str): Path to the Tinker system. Defaults to None.

        Returns:
            electric_field (list): Electric field at the point, including the magnitude.
                            Format is [E_x, E_y, E_z, |E|].
        """
        if tinker_xyz is None:
            raise ValueError("The Tinker system file must be provided.")
        else:
            tinker_xyz = os.path.abspath(tinker_xyz)
        
        # Convert list to np.ndarray if necessary
        if isinstance(point, list):
            point = np.array(point)

        # Check if point is a numpy array with the correct shape
        if not isinstance(point, np.ndarray):
            raise TypeError("Point must be a numpy array or a list.")
        
        if point.ndim != 1 or point.shape[0] != 3:
            raise ValueError("Each point must be a one-dimension 3-element array.")
        
        # Create the ElectricFieldCompute instance and compute
        compute = ElectricFieldCompute(charge_method=charge_method, tinker_xyz=tinker_xyz)
        electric_field = compute.compute_point_ef(point)

        print(f"The electric field at the each components is (MV/cm): ")
        print(f"x: {electric_field[0]}, y: {electric_field[1]}, z: {electric_field[2]}, |E|: {electric_field[3]}")

        return electric_field

    def electric_field_bond(self, charge_method: str = 'eem', tinker_xyz: str = None, bond: List[int]= None, mask:bool=True) -> float:
        """
        Compute the electric field projected at the specified bonds.

        Args:
            charge_method (str, optional): The charge method. Defaults to 'eem'. (eem, qeq, qtpie)
            tinker_xyz (str): Path to the Tinker system. Defaults to None.
            bond (List[int]): The bonds where the electric field is projected.
            mask (bool): Whether to mask the electric field generated by self. Defaults to True.

        Returns:
            bond_electric_field: Electric field projected along the bond.
        """
        if tinker_xyz is None:
            raise ValueError("The Tinker system file must be provided.")
        else:
            tinker_xyz = os.path.abspath(tinker_xyz)
        
        if bond is None:
            raise ValueError("The bond must be provided.")
        
        # Check if bond length is 2
        if len(bond) != 2:
            raise ValueError("Bond must define exactly two atoms.")


        # Create the ElectricFieldCompute instance and compute
        compute = ElectricFieldCompute(charge_method=charge_method, tinker_xyz=tinker_xyz)
        bond_electric_field = compute.compute_bond_ef(bond,mask)

        print("The electric field projected along the bond is (MV/cm): ")
        print(bond_electric_field)

        return bond_electric_field
    
    def electric_field_grid(self, charge_method: str = 'eem', tinker_xyz: str = None, point: Union[np.ndarray, List[float]] = None,
                            center_atom:int=None , radius: float = 5.0, density_level: int = 3, if_output: bool = True, output_prefix: str = 'TKM')-> List[List[float]]:
        """
        Compute the electric field projected at the specified grid points.

        Args:
            charge_method (str, optional): The charge method. Defaults to 'eem'. (eem, qeq, qtpie)
            tinker_xyz (str): Path to the Tinker system. Defaults to None.
            point (Union[List,float]): The points where is the center of the grid.
            radius (float): The radius of the grid. Defaults to 5.0 Angstrom.
            density_level (int): The density level of the grid. Defaults to 3. (1:5, 2:10, 3:20, 4:50, 5:100, Grid Number Per Angstrom)
            if_output (bool, optional): Whether to output the DX files for the electric field components and magnitude.
            output_prefix (str, optional): The prefix for the Pymol output (.dx) files.

        Returns:
            grid_electric_field: List of electric field results at each grid point.
                    Each element is [x, y, z, E_x, E_y, E_z, |E|].
            Output the DX files for the electric field components and magnitude into the current directory.
        """
        if tinker_xyz is None:
            raise ValueError("The Tinker system file must be provided.")
        else:
            tinker_xyz = os.path.abspath(tinker_xyz)
        
        try:
            radius = float(radius)
        except ValueError:
            raise ValueError("The radius must be a float.")
        
        if center_atom is None and point is None:
            raise ValueError("The center atom index or the center point coordinate must be provided.")
        
        if point is not None and center_atom is not None:
            raise ValueError("You can only provide either the center atom index or the center point coordinate, not both of them.")
        
        if point is not None:
            if isinstance(point, list):
                point = np.array(point)
            
            if point.ndim != 1 or point.shape[0] != 3:
                raise ValueError("The center point must be a 3-element array.")
        
        if center_atom is not None:
            if not isinstance(center_atom, int):
                try:
                    center_atom = int(center_atom)
                except:
                    raise TypeError("The center atom index must be an integer.")
        
        # Create the ElectricFieldCompute instance and compute
        compute = ElectricFieldCompute(charge_method=charge_method, tinker_xyz=tinker_xyz)
        
        # Get the center point
        if center_atom is not None:
            # The center atom index is 0-based
            point = compute.tinker_system_charged.AtomCrds[center_atom-1]

        grid_electric_field = compute.compute_grid_ef(point=point, radius=radius, density_level=density_level, if_output=if_output, output_prefix=output_prefix)

        return grid_electric_field
    
    def electric_field_point_traj(self, point: Union[List, np.ndarray], charge_method: str = 'eem', 
                            tinker_xyz: str = None, tinker_arc:str = None, output:str=None, otf:bool=False) -> List[List[float]]:
        """
        Compute the electric field at the specified points.

        Args:
            point (Union[List,np.ndarray]): The points where the electric field is computed.
            charge_method (str, optional): The charge method. Defaults to 'eem'. (eem, qeq, qtpie)
            tinker_xyz (str): Path to the Tinker system. Defaults to None.
            tinker_arc (str): Path to the Tinker trajectory file. Defaults to None.
            output (str): The output file path. Defaults to None.
            otf (bool): Whether to compute charge on the fly. Defaults to False.
            
        Returns:
            electric_field (list): Electric field at the point, including the magnitude.
                            Format is [E_x, E_y, E_z, |E|].
        """
        if tinker_xyz is None:
            raise ValueError("The Tinker system file must be provided.")
        else:
            tinker_xyz = os.path.abspath(tinker_xyz)
        
        if tinker_arc is None:
            raise ValueError("The Tinker trajectory file must be provided.")
        else:
            tinker_arc = os.path.abspath(tinker_arc)
        
        # Convert list to np.ndarray if necessary
        if isinstance(point, list):
            point = np.array(point)

        # Check if point is a numpy array with the correct shape
        if not isinstance(point, np.ndarray):
            raise TypeError("Point must be a numpy array or a list.")
        
        if point.ndim != 1 or point.shape[0] != 3:
            raise ValueError("Each point must be a one-dimension 3-element array.")
        
        # Create the ElectricFieldCompute instance and compute
        compute = ElectricFieldComputeTraj(charge_method=charge_method, tinker_xyz=tinker_xyz,tinker_arc=tinker_arc)
        electric_field = compute.compute_point_ef_traj(point=point,output=output)

        return electric_field

    def electric_field_bond_traj(self, bond: List[int]= None, charge_method: str = 'eem', 
                        tinker_xyz: str = None, tinker_arc:str = None, mask:bool=True,
                        output:str=None, otf:bool=False) -> List[float]:
        """
        Compute the electric field at the specified points.

        Args:
            bond (List[int]): The bonds where the electric field is projected.
            charge_method (str, optional): The charge method. Defaults to 'eem'. (eem, qeq, qtpie)
            tinker_xyz (str): Path to the Tinker system. Defaults to None.
            tinker_arc (str): Path to the Tinker trajectory file. Defaults to None.
            mask (bool): Whether to mask the electric field generated by self. Defaults to True.
            output (str): The output file path. Defaults to None.
            otf (bool): Whether to compute charge on the fly. Defaults to False.
            
        Returns:
            electric_field (list):  Electric field projected along the bond.
        """
        if tinker_xyz is None:
            raise ValueError("The Tinker system file must be provided.")
        else:
            tinker_xyz = os.path.abspath(tinker_xyz)
        
        if tinker_arc is None:
            raise ValueError("The Tinker trajectory file must be provided.")
        else:
            tinker_arc = os.path.abspath(tinker_arc)
        
        # Create the ElectricFieldCompute instance and compute
        compute = ElectricFieldComputeTraj(charge_method=charge_method, tinker_xyz=tinker_xyz,tinker_arc=tinker_arc)
        electric_field = compute.compute_bond_ef_traj(bond=bond,mask=mask,output=output,on_the_fly=otf)

        return electric_field




if __name__ == '__main__':
    control = 12
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
    # RMSD
    elif control == 6:
        output = tkm.rmsd(xyz=r'/home/wayne/quanmol/TinkerModellor/example/rmsd/pr_coord.xyz',\
                        arc = r'/home/wayne/quanmol/TinkerModellor/example/rmsd/pr_coord.arc',
                        ndx=[51,45,12,64,53,21,74])
    
    # Distance
    elif control == 7:
        output, avg_output = tkm.distance(xyz=r'/home/wayne/quanmol/TinkerModellor/example/rmsd/pr_coord.xyz',\
                        arc = r'/home/wayne/quanmol/TinkerModellor/example/rmsd/pr_coord.arc',
                        ndx=[51,51])
        
    # Distance
    elif control == 8:
        output, avg_output = tkm.angle(xyz=r'example/rmsd/pr_coord.xyz',\
                        arc = r'example/rmsd/pr_coord.arc',
                        ndx=[51,46,74])
        
    # TK2PDB
    elif control == 9:
        tkm.tk2pdb(r'example/tk2pdb/ex1/tinker.xyz',\
                r'example/tk2pdb/ex1/tk2pdb.pdb')
    
    # Electric Field
    elif control == 10:
        tkm.electric_field()

    # electric_field_point_traj
    elif control == 11:
        tkm.electric_field_point_traj(point=[0.0, 0.0, 0.0], charge_method='eem', tinker_xyz='example/ef/traj/ex1/ke15_1.xyz', tinker_arc='example/ef/traj/ex1/ke15_1.arc')
    
    # electric_field_bond_traj
    elif control == 12:
        tkm.electric_field_bond_traj(charge_method='eem', tinker_xyz='example/ef/traj/ex1/ke15_1.xyz', tinker_arc='example/ef/traj/ex1/ke15_1.arc', bond=[1, 2])

