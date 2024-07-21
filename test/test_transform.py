import pytest
from tinkermodellor import TinkerModellor as tkm
from tinkermodellor.build.system.tinker._tinkersystem import TinkerSystem

#Protein&water : '1ALB','1BHZ','134L'
#Special residual : 'ASP','CYX'(two chains is not supported yet),'GLU','HIS','LYS'
#Protein&substrate : '1AM6','3HTB'$Will be supported latter
@pytest.mark.parametrize('data',['1ALB','1BHZ','134L'])
def test_transform(data, get_file_path):
    tkm_toolkit = tkm()
    """
    1.get the file path
    2.transform the gmx-file to tinker-file and create a [tinker-system]Class-A
    3.[tinker-system]Class-A check it self
    4.read the output tinker-file to [tinker-system]Class-B
    5.[tinker-system]Class-B check it self
    """
    gro, top ,xyz= get_file_path(data)
    tinker_system_1_1 = tkm_toolkit.transform(gmx_gro=gro,gmx_top=top,tinker_xyz=xyz)
    tinker_system_1_1.check()
    tinker_system_1_2 = TinkerSystem()
    tinker_system_1_2.read_from_tinker(xyz)
    tinker_system_1_2.check()
