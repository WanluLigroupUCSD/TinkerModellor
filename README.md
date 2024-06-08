
# TinkerModellor

***An Efficient Tool for Building Biological Systems in Tinker Simulations***

## Description

TinkerModellor (TKM) serves as a versatile biological system construction tool designed to create intricate virtual biological systems for molecular dynamics within the Tinker Simulation Program. Its primary function involves the input generation of complex systems compatible with molecular simulation software. TKM possesses the capability to convert various specific formats, such as crd/top in Amber, gro/top in GROMACS, and crd/psf in CHARMM, into the Tinker format (Tinker XYZ). Moreover, TKM offers a user-friendly and concise approach, functioning as an independent script for convenient usability. Additionally, it provides users with several distinct modules to construct personalized workflows, ensuring flexibility and ease of use. Essentially, TKM empowers users to model or simulate within one software and seamlessly transition to Tinker for analysis or further simulation, effectively harnessing separate functionalities concurrently.

## Installing TinkerModellor

Firstly, you can to download it through git or zip file

```bash
# in terminal
git clone git@github.com:Hsuchein/TinkerModellor.git
```

Then go into the TinkerModellor folder, construct environment for TinkerModellor by conda

```bash
cd TinkerModellor.
conda env create -n tkm -f env.yml
conda activate tkm
```

Additionally, TinkerModellor is based on ParmEd programme. Hence, you also need to install ParmEd

```bash
git clone git@github.com:ParmEd/ParmEd.git
cd ParmEd
pip install .
```

Ultimately, install the TinkerModellor

```bash
cd TinkerModellor
export TKMROOT=$(pwd)
#direct to current directory
```

## Building

To build TinkerModellor, execute the following code in the terminal:

```bash
cd TinkerModellor
python -m build > build.log
```

This step will generate a folder called dist, which contains .whl file for environment setup.

```bash
# "$ tail -n 1 build.log" gets the last line of log file build.log
# which looks like "Successfully built tinkermodellor-1.1.tar.gz and TinkerModellor-1.1-cp39-cp39-linux_x86_64.whl"
# the last line was then counted by "$ wc -w ", the words number then transmit into *cut* command as the location parameter
# then cut split the last line and feedback the last words,which is the *.whl file
# finally, the *.whl file was pip install
pip install dist/$(tail -n 1 build.log |cut -d ' ' -f $(tail -n 1 build.log |wc -w))
```

A successful installation will look like the following:

``` bash
#Processing ./dist/TinkerModellor-1.1-cp39-cp39-linux_x86_64.whl
#Installing collected packages: TinkerModellor
#Successfully installed TinkerModellor-1.1
```

## Testing

To automatically run the TinkerModelling tests, execute the following code in the terminal:

``` sh
cd test
pytest . -v
```

## Usage

### Command Line Usage

#### The general usage of the command is as follows:

``` python
python tkm.py -c coordination_file -p topology_file -out output_file [options]
```

#### Arguments

**-c**: Path to the coordination file. Supported formats: Amber(.inpcrd/.crd), CHARMM(.crd), GROMACS(.gro). This argument is required.

**-p**: Path to the topology file. Supported formats: Amber(.prmtop/.top), CHARMM(.psf), GROMACS(.top). This argument is required.

**-o**: Output file path or name. Default is "./TinkerModellor.xyz". The format is tinker(.xyz).

**-k**: Option to keep temporary files created during GROMACS format conversion. Set to True to keep. Default is False.

**-f**: Input file format. Options: {A: Amber, C: CHARMM, G: GROMACS}. Default is GROMACS.

**-a**: Aggressive atomtype matching mode. May result in atomtype mismatching but can match irregular atomtypes. Default is True.

#### Example

Here is an example of how to use the command:

``` python
python tkm.py -c my_coordination_file.gro -p my_topology_file.top -o my_output_file.xyz -f G -a True
```

This command will run the TinkerModellor with a GROMACS coordination file my_coordination_file.gro and topology file my_topology_file.top, and it will output the result to my_output_file.xyz. The input file format is set to GROMACS, and the aggressive atomtype matching mode is enabled

### Packge Usage

``` python
# in python
import tinkermodellor as tkm
new= tkm()
new('gromacs.gro',gromacs.top')
new.write_tkmsystem('gromacs.xyz')
```

## Authors and Contributors

The following people have contributed directly to the coding and validation efforts in Tinkermodellor. And a special thanks to all of you who helped improve this project either by providing feedback, bug reports, or other general comments!

Xujian Wang |   <Hsuchein0126@outlook.com>

Haodong Liu |   <haodonliu@foxmail.com>

Wanlu Li    |   <wa1019@ucsd.edu>

The TKM-1.0 version repository(Older version, not maintained currently):
<https://github.com/Hsuchein/TinkerModellor>

## License

**it under the terms of the BSD 3-Clause License** Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions, and the following
disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions, and the following
disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written permission.

see more information in the license file.

## Citation

Please site the website if you use this software in your research:
<https://github.com/WanluLigroupUCSD/TinkerModellor>

## Reference

**Parmed**  <https://github.com/ParmEd/ParmEd>
