import pytest
import os
from tinkermodellor import TinkerModellor as tkm


TINKER_XYZ = r'\s*[0-9]*\s*[a-zA-Z0-9]*\+?-?\s*\+?-?[0-9]+.[0-9]+\s+\+?-?[0-9]+.[0-9]+\s+\+?-?[0-9]+.[0-9]+\s+[0-9A-Za-z]+\s*[0-9]*\s*[0-9]*\s*[0-9]*\s*[0-9]*\n'
system = tkm()

print('---Testing the transformers---')

#Protein&water : '1ALB','1BHZ','134L'
#Protein&substrate : '1AM6','3HTB'

@pytest.mark.parametrize('data', ['1ALB','1BHZ','134L'])
def test_atom_align_dict(data, get_file_path):
    """Test that both __call__ and map methods return the expected atom map."""
    gro, top = get_file_path(data)
    xyz  = os.path.join(pytest.OUTPUT_PATH, f"{data}.xyz")
    print("",f'Task: {data} will be tested','gro_input:',gro,'top_input:',top,'xyz_output:',xyz,sep='\n$ ')
    tinker_system = system.transform(gmx_gro=gro,gmx_top=top,tinker_xyz=xyz)
    tinker_system.check()



