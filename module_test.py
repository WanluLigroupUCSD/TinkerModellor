from tinkermodellor.build import GMXSystem
from tinkermodellor.build import TinkerSystem

if __name__ == '__main__':

    control = 1

    if control == 0:
        gmx = GMXSystem()
        gmx.read_gmx_file(r'/home/wayne/quanmol/TinkerModellor/example/gromacs.gro', \
            r'/home/wayne/quanmol/TinkerModellor/example/gromacs.top')
    elif control == 1:
        tk = TinkerSystem()
        tk.read_from_tinker(r'/home/wayne/quanmol/TinkerModellor/example/gromacs.xyz')
        tk.write(r'/home/wayne/quanmol/TinkerModellor/example/tinker.xyz')