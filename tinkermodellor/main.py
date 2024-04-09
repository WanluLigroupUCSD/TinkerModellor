"""TinkerModellor main module.
"""

import argparse

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
        '--clean', type=str, default=True,
        help='Keep temporary files created during GROMACS format conversion.\n \
        Set to False to keep.\nDefault: True')
    transform.add_argument(
        '--format', type=str, default='GROMACS',
        choices=['AMBER', 'GROMACS', 'CHARMM'],
        help='Select input file format (default: GROMACS)'
    )


    return p.parse_args()

   
def main():
    args = parse_args()
    if args.module == 'transform':
        from tinkermodellor import TinkerModellor

        tkm = TinkerModellor()
        tkm.transform(args.crd, args.top, args.xyz)

