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
        help='Path to the topology file.Supported formats:\n \
        Amber(.prmtop/.top), CHARMM(.psf), GROMACS(.top)'
    )
    transform.add_argument(
        '--crd', type=str, required=True,
        help='Path to coordination file. Supported formats:\n \
        Amber(.inpcrd/.crd), CHARMM(.crd), GROMACS(.gro)'
    )
    transform.add_argument(
        '--xyz', type=str, default=None,
        help='Path to output Tinker .xyz file'
    )
    transform.add_argument(
        '--clean', default=False, action='store_true',
        help='Keep temporary files created during GROMACS format conversion.\n \
        Use --clean to cleam.\nDefault: False')
    transform.add_argument(
        '--format', type=str, default='GROMACS',
        choices=['amber','gmx','charmm'],
        help='Select input file format (default: GROMACS)'
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

    if args.module == 'transform':
        from tinkermodellor import TinkerModellor
        from tinkermodellor import ParmEd2GMX
        
        parm = ParmEd2GMX()
        crd, top = parm(args.crd, args.top, args.format)
        tkm = TinkerModellor()
        tkm.transform(crd, top, args.xyz)

        if args.clean:
            os.remove(crd)
            os.remove(top)

