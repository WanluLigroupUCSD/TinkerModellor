from tinkermodellor.model_build._tkm import TinkerModellor
import argparse
import os
import parmed as pmd

if __name__ == '__main__':
    print('\n')

    description = 'TinkerModellor: A complicated biological system construction tool for Tinker Simulation Programme'
    usage = 'python tkm.py -c coordination_file -p topology_file -out output_file [options]'
    
    parser = argparse.ArgumentParser(description=description, usage=usage,formatter_class=argparse.RawTextHelpFormatter,)
    
    parser.add_argument('-c',
                        type = str,
                        metavar = '',
                        help ='Path to the coordination file.\nSupported formats: Amber(.inpcrd/.crd), CHARMM(.crd), GROMACS(.gro)',
                        required = True)

    parser.add_argument('-p',
                        type = str,
                        metavar = '',
                        help = 'Path to the topology file.\nSupported formats: Amber(.prmtop/.top), CHARMM(.psf), GROMACS(.top)', 
                        required = True)

    parser.add_argument('-o', 
                        type = str,
                        metavar = '',
                        default= os.path.join(os.getcwd(),'/TinkerModellor.xyz'),
                        help = 'Output file path or name.\nDefault: "./TinkerModellor.xyz"\nFormat: tinker(.xyz)', 
                        )

    parser.add_argument('-k', 
                        type = str,
                        metavar = '',
                        default = False,
                        help = 'Keep temporary files created during GROMACS format conversion.\nSet to True to keep.\nDefault: False', 
                        )

    parser.add_argument('-f',
                        type = str,
                        metavar = '',
                        choices = ['A','C','G'],
                        default = 'G' ,
                        help = 'Input file format.\nOptions: {A: Amber, C: CHARMM, G: GROMACS}\nDefault: G', 
                        )

    parser.add_argument('-a',
                        type = str,
                        metavar = '',
                        default = True ,
                        help = 'Aggressive atomtype matching mode.\nMay result in atomtype mismatching but can match irregular atomtypes.\nDefault: True', 
                        )

    top_file = '/home/wayne/quanmol/TinkerModellor/test/dataset/1BHZ/gromacs.top'
    gro_file = '/home/wayne/quanmol/TinkerModellor/test/dataset/1BHZ/gromacs.gro'
    out_file = '/home/wayne/quanmol/TinkerModellor/tinker.xyz'
    tkm= TinkerModellor()
    tkm(top_file=top_file,gro_file=gro_file)
    tkm.write_tkmsystem(xyz_path=out_file)
'''      
    args = parser.parse_args()
    top_file = args.Topology_file
    gro_file = args.Coordination_file
    out_file = args.Output_file
    program = args.Format
    
    keep = args.Keep
    keep_flag = False
    if isinstance (keep,str):
        if keep.upper in ['TRUE','KEEP']:
            keep_flag = True
    
    Aggressive =args.Aggressive
    aggressive_flag = True
    if isinstance (Aggressive,str):
        if keep.upper == 'FALSE':
            aggressive_flag = False

    tkm= TinkerModellor(aggressive=aggressive_flag)

    if program == 'GROMACS' :

        tkm(top_file=top_file,gro_file=gro_file)
        tkm.write_tkmsystem(xyz_path=out_file)

    if program == 'CHARMM' or program == 'AMBER' :

        charmm = pmd.load_file(top_file,gro_file)
        charmm.save('./temp.gro')
        charmm.save('./temp.top')
      
        topology_file = './temp.top'
        coordination_file = './temp.gro'
        tkm(top_file=topology_file,gro_file=coordination_file)
        tkm.write_tkmsystem(xyz_path=out_file)

        if keep_flag:
            os.remove('./temp.gro')
            os.remove('./temp.top')
'''  

