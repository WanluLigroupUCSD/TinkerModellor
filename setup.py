#!/usr/bin/env python
"""The setup script."""

import os
from setuptools import find_packages, setup, Extension
import pybind11
import sysconfig


base_dir = os.getenv('TKMROOT', os.path.dirname(os.path.abspath(__file__)))
cpp_include_path = os.path.join(base_dir, 'src', 'include')
python_include_path = sysconfig.get_path('include')
print("Include path:", cpp_include_path)
print('Python include path:', python_include_path)
print(f'Pybind11 include path: {pybind11.get_include()}')
# cpp module
ext_modules = [
    Extension(
        'tinkermodellor.tkmtoolkit',
        [
            'src/func/tkmtoolkit.cpp',
            'src/func/rmsd.cpp',
            'src/func/distance.cpp',
            'src/func/angle.cpp'
        ],
        include_dirs=[
            pybind11.get_include(),
            python_include_path,
            cpp_include_path,
        ],
        language='c++',
        extra_compile_args=['-std=c++11', '-O3', '-Wall', '-shared', '-fPIC',],
        extra_link_args=['-shared']
    ),
]


setup(
    author="Xujian Wang, Junhong Li and Haodong Liu",
    author_email= "Hsuchein0126@outlook.com",
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
