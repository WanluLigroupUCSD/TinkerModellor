from typing import Any
import parmed as pmd
import os
from typing import Tuple

class ParmEd2GMX():
    """
    This is used to convert between different molecular file formats
    Based on ParmEd Project on Github, https://github.com/ParmEd/ParmEd
    """
    
    def __init__(self):
        pass

    def __call__(self, crd:str, top:str, format:str) -> Tuple[str, str]:
        """
        Convert AMBER or CHARMM format to GROMACS format

        args:
            crd: str: path to the coordinate file
            top: str: path to the topology file
            format: str: format of input files, either 'GMX', 'AMBER', or 'CHARMM'

        returns:
            Tuple[str, str]: path to the converted coordinate and topology files
        """
        
        crd = os.path.abspath(crd)
        top = os.path.abspath(top)

        if os.path.exists('TKM_temp.top.backup'):
            print('Removing TKM_temp.top.backup')
            os.remove('TKM_temp.top.backup')
        if os.path.exists('TKM_temp.gro.backup\n'):
            os.rename('TKM_temp.gro.backup')

        if os.path.exists('TKM_temp.top'):
            print('TKM_temp.top already exists, renaming to TKM_temp.top.backup')
            os.rename('TKM_temp.top', 'TKM_temp.top.backup')
        if os.path.exists('TKM_temp.gro'):
            print('TKM_temp.gro already exists, renaming to TKM_temp.gro.backup\n')
            os.rename('TKM_temp.gro', 'TKM_temp.gro.backup')


        format = format.upper()    
        if format == 'GMX' or format == 'GROMACS':
            # convert AMBER topology to GROMACS, CHARMM formats
            gromacs = pmd.load_file(top, crd)
            # Save a GROMACS topology and GRO files
            gromacs.save('TKM_temp.top')
            gromacs.save('TKM_temp.gro')
            crd = os.path.join(os.getcwd(), 'TKM_temp.gro')
            top = os.path.join(os.getcwd(), 'TKM_temp.top')
        elif format == 'AMBER':
            # convert AMBER topology to GROMACS, CHARMM formats
            amber = pmd.load_file(top, crd)
            # Save a GROMACS topology and GRO files
            amber.save('TKM_temp.top')
            amber.save('TKM_temp.gro')
            crd = os.path.join(os.getcwd(), 'TKM_temp.gro')
            top = os.path.join(os.getcwd(), 'TKM_temp.top')
        elif format == 'CHARMM':
            charmm = pmd.load_file(top, crd)
            charmm.save('TKM_temp.top')
            charmm.save('TKM_temp.gro')
            crd = os.path.join(os.getcwd(), 'TKM_temp.gro')
            top = os.path.join(os.getcwd(), 'TKM_temp.top')

        print(f'ParmEd2GMX Module Generation: \n\
              coordination file: {crd} \n\
              topology file :    {top} \n')
        return crd, top
    
if __name__ == '__main__':
    parm = ParmEd2GMX()
    print(parm(r'/home/wayne/quanmol/TinkerModellor/example/amber_format/solvate.inpcrd', \
               r'/home/wayne/quanmol/TinkerModellor/example/amber_format/solvate.prmtop', 'AMBER'))

        
        