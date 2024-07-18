import pytest
import random
import os
from tinkermodellor import TinkerModellor as tkm
from tinkermodellor.build.system.tinker._tinkersystem import TinkerSystem

#Protein&water : '1ALB','1BHZ','134L'
#Special residual : 'ASP','CYX'(two chains is not supported yet),'GLU','HIS','LYS'
#Protein&substrate : '1AM6','3HTB'$Will be supported latter
@pytest.mark.parametrize('data', ['ASP','1ALB','1BHZ','134L','GLU','HIS','LYS'])
def test_transform(data, get_file_path):
    tkm_toolkit = tkm()
    """Test that both __call__ and map methods return the expected atom map."""
    #got path
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
        assert deleted_atom_crd[0] != tinker_system_2.AtomCrds[index][0]
    assert len(set(random_index)) == (tinker_system_2_0.AtomNums - tinker_system_2.AtomNums)
