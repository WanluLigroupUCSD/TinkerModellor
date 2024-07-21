import pytest
import random
import os
from tinkermodellor import TinkerModellor as tkm
from tinkermodellor.build.system.tinker._tinkersystem import TinkerSystem

#Protein&water : '1ALB','1BHZ','134L'
#Special residual : 'ASP','CYX'(two chains is not supported yet),'GLU','HIS','LYS'
#Protein&substrate : '1AM6','3HTB'$Will be supported latter
@pytest.mark.parametrize('data', ['HIS','1ALB','1BHZ','134L','ASP','GLU','LYS'])
def test_delete(data, get_file_path):
    tkm_toolkit = tkm()
    """
    1.get the file path
    2.transform the tinker-file and create [tinker-system]Class-A
    3.create a random index list(maybe have same index)
    4.Use TKM delete part to remove atom in [tinker-system]Class-A via random index list and produce tinker-files
    5.check the tinker-file and create [tinker-system]Class-B
    6.check the atom number and atom crd in [tinker-system]Class-A and Class-B
    6-1. index atom_crd shouldnt be same
    6-2. atom number should be gap 
    """
    gro, top ,xyz= get_file_path(data)
    delete_file = os.path.join(pytest.OUTPUT_PATH,data+'_del.xyz')

    tinker_system_2_0 = TinkerSystem()
    tinker_system_2_0.read_from_tinker(xyz)
    former_atom_crd = tinker_system_2_0.AtomCrds

    random_index = [random.randint(1, tinker_system_2_0.AtomNums) for _ in range(random.randint(1, 10))]

    tkm_toolkit.delete(tk=xyz,index=random_index,tinker_xyz=delete_file)

    tinker_system_2 = TinkerSystem()
    tinker_system_2.read_from_tinker(delete_file)
    tinker_system_2.check()

    
    for index in random_index:
        deleted_atom_crd = former_atom_crd[index]
        X = (deleted_atom_crd[0] != tinker_system_2.AtomCrds[index][0])
        Y = (deleted_atom_crd[1] != tinker_system_2.AtomCrds[index][1])
        Z = (deleted_atom_crd[2] != tinker_system_2.AtomCrds[index][2])
        assert X or Y or Z , "index atom_crd shouldnt be same"
    assert len(set(random_index)) == (tinker_system_2_0.AtomNums - tinker_system_2.AtomNums)
