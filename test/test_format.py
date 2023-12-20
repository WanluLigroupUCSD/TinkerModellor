import pytest
import re
import os

from tinkermodellor import TinkerModellor as tkm


TINKER_XYZ = r'\s*[0-9]*\s*[a-zA-Z0-9]*\+?-?\s*\+?-?[0-9]+.[0-9]+\s+\+?-?[0-9]+.[0-9]+\s+\+?-?[0-9]+.[0-9]+\s+[0-9A-Za-z]+\s*[0-9]*\s*[0-9]*\s*[0-9]*\s*[0-9]*\n'

system = tkm()

@pytest.mark.parametrize('data', 
    ['1ALB','1BHZ','134L'])
def test_atom_align_dict(data, get_file_path):
    """Test that both __call__ and map methods return the expected atom map."""
    gro, top = get_file_path(data)
    
    system(gro,top)
    
    # Write output to a file
    output_file  = os.path.join(pytest.OUTPUT_PATH, f"{data}.xyz")
    system.write_tkmsystem(output_file)

    # Read the file content
    with open(output_file, 'r') as file:
        file_content = file.readlines()

        # Check the number of atoms
        AtomNums = int(file_content[0].strip().split(' ')[0])
        assert AtomNums == len(file_content[1:])

        # Check the format of file
        for line in file_content[1:]:
            assert re.fullmatch(TINKER_XYZ, line)

