import argparse
import os
import parmed as pmd
from tinkermodellor.model_build._tkm import TinkerModellor

if __name__ == '__main__':
    print('\n')

    description = 'TinkerModellor: A complicated biological system construction tool for Tinker Simulation Programme'
    usage = 'python tkm.py -c coordination_file -p topology_file -o output_file [options]'
    
    parser = argparse.ArgumentParser(description=description, usage=usage, formatter_class=argparse.RawTextHelpFormatter)
    
    # 定义-c和-p参数，不变
    parser.add_argument('-c', type=str, required=True, metavar='', help='Path to the coordination file.\nSupported formats: Amber(.inpcrd/.crd), CHARMM(.crd), GROMACS(.gro)')
    parser.add_argument('-p', type=str, required=True, metavar='', help='Path to the topology file.\nSupported formats: Amber(.prmtop/.top), CHARMM(.psf), GROMACS(.top)')

    # 修改-o参数的默认值设置方式
    parser.add_argument('-o', type=str, metavar='', default=os.path.join(os.getcwd(),'TinkerModellor.xyz'), help='Output file path or name.\nDefault: "./TinkerModellor.xyz"\nFormat: tinker(.xyz)')

    # 定义其他参数，不变
    parser.add_argument('-k', type=str, metavar='', default=False, help='Keep temporary files created during GROMACS format conversion.\nSet to True to keep.\nDefault: False')
    parser.add_argument('-f', type=str, metavar='', choices=['A', 'C', 'G'], default='G', help='Input file format.\nOptions: {A: Amber, C: CHARMM, G: GROMACS}\nDefault: G')
    parser.add_argument('-a', type=str, metavar='', default=True, help='Aggressive atomtype matching mode.\nMay result in atomtype mismatching but can match irregular atomtypes.\nDefault: True')

    args = parser.parse_args()

    # 这里需要按照实际使用的参数名称来获取参数值
    top_file = args.p  # 这里应该是args.p，而非args.Topology_file
    gro_file = args.c  # 这里应该是args.c，而非args.Coordination_file
    out_file = args.o  # 这里应该是args.o，而非args.Output_file

    tkm = TinkerModellor()
    tkm(top_file=top_file, gro_file=gro_file)
    tkm.write_tkmsystem(xyz_path=out_file)

'''      

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

