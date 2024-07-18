import pytest
import os
from tinkermodellor import TinkerModellor as tkm
from tinkermodellor.build.system.tinker._tinkersystem import TinkerSystem

#Protein&water : '1ALB','1BHZ','134L'
#Special residual : 'ASP','CYX'(two chains is not supported yet),'GLU','HIS','LYS'
#Protein&substrate : '1AM6','3HTB'$Will be supported latter
@pytest.mark.parametrize('data',['ASP','1ALB','1BHZ','134L','GLU','HIS','LYS'])
def test_transform(data, get_file_path):
    tkm_toolkit = tkm()
    """Test that both __call__ and map methods return the expected atom map."""
    gro, top ,xyz= get_file_path(data)
    tinker_system_1_1 = tkm_toolkit.transform(gmx_gro=gro,gmx_top=top,tinker_xyz=xyz)
    tinker_system_1_1.check()
    tinker_system_1_2 = TinkerSystem()
    tinker_system_1_2.read_from_tinker(xyz)
    tinker_system_1_2.check()
