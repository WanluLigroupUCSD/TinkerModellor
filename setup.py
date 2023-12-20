#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

setup(
    author="Xujian Wang, Haodong Liu",
    description="TinkerModellor",
    name='tinkermodellor',
    packages=find_packages(
        include=['tinkermodellor', 'tinkermodellor.*', 'tinkermodellor.*.*']),
    include_package_data=True,
    version='0.1',
    python_requires='>=3.6',
    url='https://github.com/Hsuchein/TinkerModellor',
)
