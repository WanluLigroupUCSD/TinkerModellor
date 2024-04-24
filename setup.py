#!/usr/bin/env python
"""The setup script."""

import os
from setuptools import find_packages, setup, Extension
import pybind11

base_dir = os.path.dirname(os.path.abspath(__file__))
cpp_include_path = os.path.join(base_dir, 'tinkermodellor', 'cpp_src', 'include')

# cpp module
ext_modules = [
    Extension(
        'tinkermodellor.tkmcpptoolkit',  # Python模块完整路径
        ['tinkermodellor/build/cpp_src/src/rmsd.cpp'],  # C++ 源文件相对路径
        include_dirs=[
            pybind11.get_include(),  # pybind11头文件路径
            '/home/wayne/miniconda3/envs/tkm/include',
            cpp_include_path,  
        ],
        language='c++',
        extra_compile_args=['-std=c++11', '-O3', '-Wall', '-shared', '-fPIC'],  # 添加编译标志，包括O3优化和其他必要的选项
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
    ext_modules=ext_modules,  # 将扩展模块加入到setup中
)
