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
        Use --clean to cleam.\nDefault: False')
    transform.add_argument(
        '--format', type=str, default='GROMACS',
        choices=['amber','gmx','charmm'],
        help='Select input file format (default: GROMACS)'
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
    
    print(generate_banner("Xujian Wang, Junhong Li and Haodong Liu", "TinkerModellor", "1.1",'https://github.com/WanluLigroupUCSD/TinkerModellor'))
    from tinkermodellor import TinkerModellor
    
    if args.module == 'transform':
        
        from tinkermodellor import ParmEd2GMX
        
        parm = ParmEd2GMX()
        crd, top = parm(args.crd, args.top, args.format)
        tkm = TinkerModellor()
        tkm.transform(crd, top, args.xyz)

        if args.clean:
            os.remove(crd)
            os.remove(top)
    
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