import pytest
from tinkermodellor import TinkerModellor as tkm
from tinkermodellor.build.system.tinker._tinkersystem import TinkerSystem

#Protein&water : '1ALB','1BHZ','134L'
#Special residual : 'ASP','CYX'(two chains is not supported yet),'GLU','HIS','LYS'
#Protein&substrate : '1AM6','3HTB'$Will be supported latter
#@pytest.mark.parametrize('data',['ASP','1ALB','1BHZ','134L','GLU','HIS','LYS'])
def test_merge():
    tkm_toolkit = tkm()
    """
    1.get the file path
    2.transform the gmx-file to tinker-file and create a [tinker-system]Class-A
    3.[tinker-system]Class-A check it self
    4.read the output tinker-file to [tinker-system]Class-B
    5.[tinker-system]Class-B check it self
    """

    tkm_toolkit.merge(
        tk1=r'test/example/merge/ligand.xyz',
        tk2=r'test/example/merge/protein.xyz',
        tinker_xyz=r'test/example/merge/merged_without_FF.xyz',)
    
    tinker_system_3_1 = TinkerSystem()
    tinker_system_3_1.read_from_tinker(r'test/example/merge/merged_without_FF.xyz')
    tinker_system_3_1.check()

    tkm_toolkit.merge(
        tk1=r'test/example/merge/ligand.xyz',
        tk2=r'test/example/merge/protein.xyz',
        tinker_xyz=r'test/example/merge/merged_with_FF.xyz',
        ff1=r'test/example/merge/amoebabio18.prm',
        ff2=r'test/example/merge/ligand.prm',
        ffout=r'test/example/merge/merged.prm')
    
    tinker_system_3_2 = TinkerSystem()
    tinker_system_3_2.read_from_tinker(r'test/example/merge/merged_with_FF.xyz')
    tinker_system_3_2.check()
