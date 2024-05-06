from tinkermodellor.build import GMXSystem
from tinkermodellor.build import TinkerSystem
from tinkermodellor.build import Transformer

if __name__ == '__main__':


    for control in range(3):
        if control == 0:
            gmx = GMXSystem()
            gmx.read_gmx_file(r'example\gmx_format\gromacs.gro', \
                r'example\gmx_format\gromacs.top')
        elif control == 1:
            tk = TinkerSystem()
            tk.read_from_tinker(r'example\gmx_format\gromacs.xyz')
            tk.write(r'example\gmx_format\tinker.xyz')
        elif control == 2:
            gmx = GMXSystem()
            gmx.read_gmx_file(r'example\gmx_format\gromacs.gro', \
                r'example\gmx_format\gromacs.top')
            transformer = Transformer()
            tk = transformer(gmx)
            tk.write(r'example\gmx_format\tinker.xyz')
    