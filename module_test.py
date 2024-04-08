from tinkermodellor.build import GMXSystem
from tinkermodellor.build import TinkerSystem
from tinkermodellor.build import Transformer

if __name__ == '__main__':


    for control in range(3):
        if control == 0:
            gmx = GMXSystem()
            gmx.read_gmx_file(r'/home/wayne/quanmol/TinkerModellor/example/gromacs.gro', \
                r'/home/wayne/quanmol/TinkerModellor/example/gromacs.top')
        elif control == 1:
            tk = TinkerSystem()
            tk.read_from_tinker(r'/home/wayne/quanmol/TinkerModellor/example/gromacs.xyz')
            tk.write(r'/home/wayne/quanmol/TinkerModellor/example/tinker.xyz')
        elif control == 2:
            gmx = GMXSystem()
            gmx.read_gmx_file(r'/home/wayne/quanmol/TinkerModellor/example/gromacs.gro', \
                r'/home/wayne/quanmol/TinkerModellor/example/gromacs.top')
            transformer = Transformer()
            tk = transformer(gmx)
            tk.write(r'/home/wayne/quanmol/TinkerModellor/example/tinker.xyz')
    