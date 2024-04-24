#!/usr/bin/env python
"""The setup script."""

import os
from setuptools import find_packages, setup, Extension
import pybind11
import sysconfig



base_dir = os.path.dirname(os.path.abspath(__file__))
cpp_include_path = os.path.join(base_dir, 'tinkermodellor', 'cpp_src', 'include')
python_include_path = sysconfig.get_path('include')
# cpp module
ext_modules = [
    Extension(
        'tinkermodellor.tkmtoolkit',  # Python module name
        ['tinkermodellor/build/cpp_src/src/rmsd.cpp'],  # C++ src
        include_dirs=[
            pybind11.get_include(),  # pybind11 headers
            python_include_path,
            cpp_include_path,  
        ],
        language='c++',
        extra_compile_args=['-std=c++11', '-O3', '-Wall', '-shared', '-fPIC'],  # compile args
        extra_link_args=['-shared']
    ),
]


setup(
    author="Xujian Wang, Junhong Li and Haodong Liu",
    description="TinkerModellor",
    name='tinkermodellor',
    packages=find_packages(include=['tinkermodellor', 'tinkermodellor.*']),
    include_package_data=True,
    version='1.1',
    python_requires='>=3.6',
    entry_points={'console_scripts': ['tkm = tinkermodellor.main:main']},
    url='https://github.com/Hsuchein/TinkerModellor',
    ext_modules=ext_modules, 
)
