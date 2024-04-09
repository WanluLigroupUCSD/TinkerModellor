import os

from tinkermodellor.build import TinkerSystem
from tinkermodellor.build import GMXSystem
from tinkermodellor.build import Transformer

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

if __name__ == '__main__':
    tkm= TinkerModellor()
    tkm.transform(r'/home/wayne/quanmol/TinkerModellor/example/gromacs.gro',r'/home/wayne/quanmol/TinkerModellor/example/gromacs.top')
