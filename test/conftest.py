import os
import pathlib
from typing import Tuple

import pytest


def pytest_configure():
    this_dir = pathlib.Path(__file__).parent
    pytest.EXAMPLE_PATH = str(this_dir.joinpath("dataset"))
    pytest.OUTPUT_PATH = this_dir.joinpath(".pytest_cache/")
    
    #If .pytest not exist, then create a new .pytest folder.
    pytest.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    pytest.OUTPUT_PATH = str(pytest.OUTPUT_PATH)
    

@pytest.fixture(scope='session')
def get_file_path():
    def _get_file_path(data_name) -> Tuple[str, str]:
        gro = os.path.join(pytest.EXAMPLE_PATH, data_name, 'gromacs.gro')
        top = os.path.join(pytest.EXAMPLE_PATH, data_name, 'gromacs.top')
        return (gro, top)
    return _get_file_path
