from tinkermodellor.build import GMXSystem
from tinkermodellor.build import TinkerSystem
from tinkermodellor.build import Transformer

if __name__ == '__main__':

    control = 2

    if control == 0:
        gmx = GMXSystem()
        gmx.read_gmx_file(r'./example/gromacs.gro', \
            r'./example/gromacs.top')
    elif control == 1:
        tk = TinkerSystem()
        tk.read_from_tinker(r'./example/gromacs.xyz')
        tk.write(r'./example/tinker.xyz')
    elif control == 2:
        gmx = GMXSystem()
        gmx.read_gmx_file(r'./example/gromacs.gro', \
            r'./example/gromacs.top')
        transformer = Transformer()
        tk = transformer(gmx)
        tk.write(r'./example/tinker.xyz')
    