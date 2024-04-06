from tinkermodellor.model_build._class import GMXSystem

if __name__ == '__main__':

    gmx = GMXSystem()
    gmx.read_gmx_file(r'/home/wayne/quanmol/TinkerModellor/example/gromacs.gro', \
        r'/home/wayne/quanmol/TinkerModellor/example/gromacs.top')