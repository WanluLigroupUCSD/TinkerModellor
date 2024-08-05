"""TinkerModellor main module.
"""

import argparse
import os

def parse_args():
    p = argparse.ArgumentParser('tkm')
    subparsers = p.add_subparsers(dest='module')

    # transform
    transform = subparsers.add_parser(
        'transform', help='Transform files to Tinker files',)
    transform.add_argument(
        '--top', type=str, required=True,
        help='Path to the topology file.Supported formats:\n\
        Amber(.prmtop/.top), CHARMM(.psf), GROMACS(.top)'
    )
    transform.add_argument(
        '--crd', type=str, required=True,
        help='Path to coordination file. Supported formats:\n\
        Amber(.inpcrd/.crd), CHARMM(.crd), GROMACS(.gro)'
    )
    transform.add_argument(
        '--xyz', type=str, default=None,
        help='Path to output Tinker .xyz file'
    )
    transform.add_argument(
        '--clean', default=False, action='store_true',
        help='Keep temporary files created during GROMACS format conversion.\n\
        Use --clean to clean.\nDefault: False')
    transform.add_argument(
        '--format', type=str, default='GROMACS',
        choices=['amber','gmx','charmm'],
        help='Select input file format (default: GROMACS)'
    )
    transform.add_argument(
        '--ff', type=str, default='1',
        help='Select force field type (default: 1, 1: AMOEBABIO18, 2: AMOEBABIO09,\n\
            3: AMOEBAPRO13)-protein only,4:amoebanuc17)-nuclear acid only'
    )

    # merge
    merge = subparsers.add_parser(
        'merge', help='Merge two system (force field also could be merged together).\n\
        If ff1 or ff2 or ffout is given, then the rest also should be given',)
    merge.add_argument(
        '--tk1', type=str, required=True,
        help='Path to the first TXYZ file'
    )
    merge.add_argument(
        '--tk2', type=str, required=True,
        help='Path to the second TXYZ file'
    )
    merge.add_argument(
        '--xyz', type=str, required=True,
        help='Path to the output TXYZ file'
    )
    merge.add_argument(
        '--ff1', type=str, default=None,
        help='Path to force field file of the first system (optional)'
    )
    merge.add_argument(
        '--ff2', type=str, default=None,
        help='Path to force field file of the second system (optional)'
    )
    merge.add_argument(
        '--ffout', type=str, default=None,
        help='Paht to force filed file of the output system (optional)'
    )

    # delete
    delete = subparsers.add_parser(
        'delete', help='Delete atoms from a Tinker system')
    delete.add_argument(
        '--tk', type=str, required=True,
        help='Path to the input TXYZ file'
    )
    delete.add_argument(
        '--xyz', type=str, required=True,
        help='Path to the output TXYZ file'
    )
    delete.add_argument(
        '--ndx', type=str, required=True,
        help='Index of the atoms to be deleted, could be a single integer 10,\n\
        or a list seperated by comma 1,2,3, or a range 1-10, or a combination of them 1,2,3,5-10'
    )

    # replace
    replace = subparsers.add_parser(
        'replace', help='Merge two system (force field also could be merged together).\n\
        But coincident water and ion molecules in tk1 would be deleted',)
    replace.add_argument(
        '--tk1', type=str, required=True,
        help='Path to the first TXYZ file'
    )
    replace.add_argument(
        '--tk2', type=str, required=True,
        help='Path to the second TXYZ file'
    )
    replace.add_argument(
        '--xyz', type=str, required=True,
        help='Path to the output TXYZ file'
    )
    replace.add_argument(
        '--ff1', type=str, default=None,
        help='Path to force field file of the first system (optional)'
    )
    replace.add_argument(
        '--ff2', type=str, default=None,
        help='Path to force field file of the second system (optional)'
    )
    replace.add_argument(
        '--ffout', type=str, default=None,
        help='Paht to force filed file of the output system (optional)'
    )

    # rmsd
    rmsd = subparsers.add_parser(
        'rmsd', help='Calculate the RMSD of Tinker trajectory file (.arc).',)
    rmsd.add_argument(
        '--xyz', type=str, required=True,
        help='Path to the TXYZ file (.xyz) for identifying the topology'
    )
    rmsd.add_argument(
        '--traj', type=str, required=True,
        help='Path to the Tinker trajectory file (.arc)'
    )
    rmsd.add_argument(
        '--ref', type=str,
        help='Path to the reference coordinates file (.xyz),if not given,\n\
            the first frame of the trajectory would be used as reference (optional)'
    )
    rmsd.add_argument(
        '--skip', type=str, default=None,
        help='Skip frames in the trajectory file (optional)'
    )
    rmsd.add_argument(
        '--ndx', type=str, default=None,
        help='The index of atoms to be calculated RMSD (optional), could be a single integer 10,\n\
        or a list seperated by comma 1,2,3, or a range 1-10, or a combination of them 1,2,3,5-10'
    )
    rmsd.add_argument(
        '--bfra', type=str, default='0',
        help='The begin frame of the trajectory to be calculated RMSD (optional)\n\
        Default: 0'
    )
    rmsd.add_argument(
        '--efra', type=str, default='-1',
        help='The end frame of the trajectory to be calculated RMSD (optional)\n\
        Default: the last frame of the trajectory'
    )
    rmsd.add_argument(
        '--out', type=str, default='./TKM_rmsd.csv',
        help='Path to the output CSV file. Default: ./TKM_rmsd.csv'
    )

    # distance
    distance = subparsers.add_parser(
        'distance', help='Calculate the atomic distance of Tinker trajectory file (.arc).',)
    distance.add_argument(
        '--xyz', type=str, required=True,
        help='Path to the TXYZ file (.xyz) for identifying the topology'
    )
    distance.add_argument(
        '--traj', type=str, required=True,
        help='Path to the Tinker trajectory file (.arc)'
    )
    distance.add_argument(
        '--skip', type=str, default=None,
        help='Skip frames in the trajectory file (optional)'
    )
    distance.add_argument(
        '--ndx', type=str, required=True,
        help='The index of atoms to be calculated RMSD (optional), could be a single integer 10,\n\
        or a list seperated by comma 1,2,3, or a range 1-10, or a combination of them 1,2,3,5-10'
    )
    distance.add_argument(
        '--bfra', type=str, default='0',
        help='The begin frame of the trajectory to be calculated RMSD (optional)\n\
        Default: 0'
    )
    distance.add_argument(
        '--efra', type=str, default='-1',
        help='The end frame of the trajectory to be calculated RMSD (optional)\n\
        Default: the last frame of the trajectory'
    )
    distance.add_argument(
        '--out', type=str, default='./TKM_distance.csv',
        help='Path to the output CSV file. Default: ./TKM_distance.csv'
    )

    # angle
    angle = subparsers.add_parser(
        'angle', help='Calculate the atomic angle of Tinker trajectory file (.arc).',)
    angle.add_argument(
        '--xyz', type=str, required=True,
        help='Path to the TXYZ file (.xyz) for identifying the topology'
    )
    angle.add_argument(
        '--traj', type=str, required=True,
        help='Path to the Tinker trajectory file (.arc)'
    )
    angle.add_argument(
        '--skip', type=str, default=None,
        help='Skip frames in the trajectory file (optional)'
    )
    angle.add_argument(
        '--ndx', type=str, required=True,
        help='The index of atoms to be calculated RMSD (optional), could be a single integer 10,\n\
        or a list seperated by comma 1,2,3, or a range 1-10, or a combination of them 1,2,3,5-10'
    )
    angle.add_argument(
        '--bfra', type=str, default='0',
        help='The begin frame of the trajectory to be calculated RMSD (optional)\n\
        Default: 0'
    )
    angle.add_argument(
        '--efra', type=str, default='-1',
        help='The end frame of the trajectory to be calculated RMSD (optional)\n\
        Default: the last frame of the trajectory'
    )
    angle.add_argument(
        '--out', type=str, default='./TKM_angle.csv',
        help='Path to the output CSV file. Default: ./TKM_angle.csv'
    )

    # connect
    connect = subparsers.add_parser(
        'connect', help='Connect atoms from a Tinker system')
    connect.add_argument(
        '--tk', type=str, required=True,
        help='Path to the input TXYZ file'
    )
    connect.add_argument(
        '--xyz', type=str, required=True,
        help='Path to the output TXYZ file'
    )
    connect.add_argument(
        '--ndx', type=str, required=True,
        help='Index of the atoms to be connected, could a list seperated by comma 1,2. Two atoms only.'
    )

    # tk2pdb
    tk2pdb = subparsers.add_parser(
        'tk2pdb', help='Transform Tinker XYZ file to PDB file')
    tk2pdb.add_argument(
        '--tk', type=str, required=True,
        help='Path to the input TXYZ file'
    )
    tk2pdb.add_argument(
        '--pdb', type=str, required=True,
        help='Path to the output PDB file'
    )
    tk2pdb.add_argument(
        '--depth', type=str, default='10000',
        help='Depth of search algorithm (optional), Default: 10000'
    )
    tk2pdb.add_argument(
        '--style', type=str, default='1',
        help='TXYZ style, if it is generated by TinkerModellor, then choose 1, \n\
        if it is generated by Tinker pdbxyz module, then choose 2. (Default: 1)'
    )

    # ef
    ef = subparsers.add_parser(
        'ef', help='Electric Field Calculation for Tinker XYZ file')
    ef.add_argument(
        '--type', type=str, required=True,
        help='Job type,\n \
            point (calculate electric field at a point)\n \
            grid (calculate electric field on a grid) \n \
            bond (calculate electric field projected at a bond, the direction is from the first atom to the second atom)'
    )
    ef.add_argument(
        '--tk', type=str, required=True,
        help='Path to the input TXYZ file'
    )
    ef.add_argument(
        '--chg', type=str, default=None,
        help='Charge method, could be eem ,qeq or qtpie, Default: eem'
    )
    ef.add_argument(
        '--point', type=str, default=None,
        help='The point to calculate electric field, required when type is point or gird.\n \
            use comma to separate the coordinates, e.g. 0.0,0.0,0.0'
    )
    ef.add_argument(
        '--ndx', type=str, default=None,
        help='The atom index which is the center of grid, required when type is grid.'
    )
    ef.add_argument(
        '--rad', type=float, default=5.0,
        help='The radius of the grid, required when type is grid. (Default: 5.0 Angstrom)'
    )
    ef.add_argument(
        '--den', type=int, default=3,
        help='The density of the grid, required when type is grid. (Default: 3) \n \
            (1:5, 2:10, 3:20, 4:50, 5:100, Grid Number Per Angstrom)'
    )
    ef.add_argument(
        '--out', type=str, default='TKM',
        help='The prefix of Pymol (.dx) output file, required when type is grid. Default: TKM'
    )
    ef.add_argument(
        '--bond', type=str, default=None,
        help='The atom index of the bond, required when type is bond. \n \
            use comma to separate the atom index, e.g. 1,2'
    )


    return p.parse_args()

def generate_banner(author, project_name, version, url):
    term_width = os.get_terminal_size().columns
    banner_width = 80
    title = f"{project_name} Version {version}"
    padding = ' ' * ((term_width - banner_width) // 2)

    banner = f"""
    {padding}{'*' * banner_width}
    {padding}*{author.center(banner_width-2)}*
    {padding}*{title.center(banner_width-2)}*
    {padding}*{url.center(banner_width-2)}*
    {padding}{'*' * banner_width}
    """
    return banner


def main():
    args = parse_args()
    
    print(generate_banner("Xujian Wang, Haodong Liu and Wanlu Li", "TinkerModellor", "1.1",'https://github.com/WanluLigroupUCSD/TinkerModellor'))
    from tinkermodellor import TinkerModellor
    
    if args.module == 'transform':
        
        from tinkermodellor import ParmEd2GMX
        
        parm = ParmEd2GMX()
        crd, top = parm(args.crd, args.top, args.format)
        tkm = TinkerModellor()
        tkm.transform(crd, top, args.xyz, args.ff)

        if args.clean:
            os.remove(crd)
            os.remove(top)
            transed_file = args.ff.replace('.prm', '.json')
            if os.path.exists(transed_file):
                os.remove(transed_file)
    
    elif args.module == "merge":
        
        tkm = TinkerModellor()
        tkm.merge(args.tk1, args.tk2, args.xyz, args.ff1, args.ff2, args.ffout)

    elif args.module == "delete":

        from tinkermodellor.build import parse_ndx

        tkm = TinkerModellor()
        tkm.delete(args.tk, parse_ndx(args.ndx), args.xyz, )

    elif args.module == "replace":
        
        tkm = TinkerModellor()
        tkm.replace(args.tk1, args.tk2, args.xyz, args.ff1, args.ff2, args.ffout)
    
    elif args.module == "rmsd":

        from tinkermodellor.build import parse_ndx
        from tinkermodellor.build import CSVMaker

        csv = CSVMaker()
        tkm = TinkerModellor()
        if args.ndx is not None:
            ndx = parse_ndx(args.ndx)
        else:
            ndx = None
        skip = int(args.skip) if args.skip is not None else None
        result = tkm.rmsd(args.xyz, args.traj, args.ref, skip, ndx,int(args.bfra),int(args.efra))
        csv.column_writer(result, args.out)
    
    elif args.module == "distance":

        from tinkermodellor.build import parse_ndx
        from tinkermodellor.build import CSVMaker

        csv = CSVMaker()
        tkm = TinkerModellor()
        if args.ndx is not None:
            ndx = parse_ndx(args.ndx)

            if len(ndx) != 2:
                raise ValueError("The index must contain two elements.")
        else:
            ndx = None
        skip = int(args.skip) if args.skip is not None else None
        result, _ = tkm.distance(args.xyz, args.traj, skip, ndx,int(args.bfra),int(args.efra))
        csv.column_writer(result, args.out)

    elif args.module == "angle":

        from tinkermodellor.build import parse_ndx
        from tinkermodellor.build import CSVMaker

        csv = CSVMaker()
        tkm = TinkerModellor()
        if args.ndx is not None:
            ndx = parse_ndx(args.ndx)
            if len(ndx) != 3:
                raise ValueError("The index must contain three elements.")
        else:
            raise ValueError("The index of atoms to be calculated angle is required.")
        skip = int(args.skip) if args.skip is not None else None
        result, _ = tkm.angle(args.xyz, args.traj, skip, ndx,int(args.bfra),int(args.efra))
        csv.column_writer(result, args.out)
    
    elif args.module == "connect":

        from tinkermodellor.build import parse_ndx

        tkm = TinkerModellor()
        tkm.connect(args.tk, parse_ndx(args.ndx), args.xyz)
    
    elif args.module == "tk2pdb":
            
        tkm = TinkerModellor()
        try:
            int(args.depth)
            int(args.style)
        except:
            raise ValueError("The depth or style must be integers.")
        
        tkm.tk2pdb(args.tk, args.pdb,int(args.depth), int(args.style))  

    elif args.module == "ef":
            
            from tinkermodellor.build import parse_ndx

            try:
                tinker_xyz = os.path.abspath(args.tk)
            except:
                raise ValueError("The path to the input TXYZ file is required.")
            if args.chg is None:
                print("The charge method is not given, use EEM as default.")
                charge_method = 'eem'
            else:
                if args.chg.lower() not in ['eem', 'qeq', 'qtpie']:
                    raise ValueError("The charge method must be eem, qeq or qtpie.")
                else:
                    charge_method = args.chg.lower()
    
            tkm = TinkerModellor()
            if args.type == 'point':
                if args.point is None:
                    raise ValueError("The point is required.")
                point = [float(i) for i in args.point.split(',')]

                tkm.electric_field_point(tinker_xyz=tinker_xyz, charge_method=charge_method, point=point)

            elif args.type == 'grid':
                if args.rad is None:
                    print("The radius of the grid is not given, use 5.0 as default.")
                    radius = 5.0
                else:
                    try:
                        radius = float(args.rad)
                    except:
                        raise ValueError("The radius of the grid must be a float.")
                if args.den is None:
                    print("The density of the grid is not given, use 3 as default.")
                    density = 3
                else:
                    try:
                        density = int(args.den)
                    except:
                        raise ValueError("The density of the grid must be an integer.")
                    
                if args.point is None and args.ndx is None:
                    raise ValueError("The center atom index or the center point coordinate must be provided.")
        
                if args.point is not None and args.ndx is not None:
                    raise ValueError("You can only provide either the center atom index or the center point coordinate, not both of them.")
                
                # Use the coordinate to calculate the electric field
                if args.point is not None:
                    point = [float(i) for i in args.point.split(',')]
                    tkm.electric_field_grid(tinker_xyz=tinker_xyz, charge_method=charge_method, \
                                        point=point, radius=radius, density_level=density, output_prefix=args.out)
                    
                # Specify the atom index to the center of the grid
                if args.ndx is not None:
                    tkm.electric_field_grid(tinker_xyz=tinker_xyz, charge_method=charge_method, center_atom=args.ndx, \
                                        radius=radius, density_level=density, output_prefix=args.out)
            
            elif args.type == 'bond':
                if args.bond is None:
                    raise ValueError("The bond is required.")
                else:
                    tkm.electric_field_bond(tinker_xyz=tinker_xyz, charge_method=charge_method, bond=parse_ndx(args.bond))
            else:
                raise ValueError("The type must be point, grid or bond.") 