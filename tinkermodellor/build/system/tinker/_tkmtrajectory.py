from typing import List, Union
import numpy as np
import warnings
from io import StringIO
from dataclasses import dataclass
import os
import codecs
from tqdm import tqdm
import time

from tinkermodellor.messager import (TinkerSystemReminder,TinkerTrajectoryReminder)


class TKMTrajectory:
    def __init__(self, system_name: str = None):

        self.SystemName = system_name if system_name is not None else 'TinkerModellor Default Name'
        self.AtomNums = 0
        self.AtomIndex = np.array([], dtype=int)
        self.AtomTypesStr = []
        self.AtomTypesNum = np.array([], dtype=int)
        self.Bonds = []
        self.BoxSize = np.empty((0, 3), dtype=float)
        self.BoxAngle = np.empty((0, 3), dtype=float)
        self.AtomCrds = np.empty((0, 0, 3), dtype=float)  # Initial empty array for trajectory data



    @TinkerSystemReminder
    def read_from_tinker(self, tinker_xyz: str) -> "TKMTrajectory":
        """Load molecule from input tinker xyz file."""
        file_path = os.path.abspath(tinker_xyz)
        contents = []
        with codecs.open(file_path, 'r', 'utf-8-sig') as f:
            contents = f.readlines()

        atom_nums = 0
        system_name = None
        atom_index = []
        atom_type_str = []
        atom_crds = []
        atom_type_num = []
        atom_bonds = []
        box_size = np.array([0.0, 0.0, 0.0])  # Default box size vector

        for line_idx, line in enumerate(contents):
            line = line.strip()
            if not line:
                continue

            if line_idx == 0:
                arr = line.split()
                atom_nums = int(arr.pop(0))
                system_name = " ".join(arr)
            elif line_idx == 1 and len(line.split()) == 6:
                box_size = np.array([float(x) for x in line.split()], dtype=float)
            else:
                arr = line.split()
                atom_index.append(int(arr[0]))
                atom_type_str.append(arr[1])
                atom_crds.append([float(x) for x in arr[2:5]])
                atom_type_num.append(int(arr[5]))
                atom_bonds.append([int(x) for x in arr[6:]])

        if atom_crds:
            atom_crds = np.array(atom_crds, dtype=float)
            self.AtomCrds = np.expand_dims(atom_crds, axis=0)  # Add frame dimension

        self.AtomNums = atom_nums
        self.SystemName = system_name
        self.AtomIndex = np.array(atom_index, dtype=int)
        self.AtomTypesStr = atom_type_str
        self.AtomTypesNum = np.array(atom_type_num, dtype=int)
        self.Bonds = atom_bonds
        self.BoxSize = box_size

        print(f'This Tinker system contains {self.AtomNums} atoms.')
        return self
  
    @TinkerTrajectoryReminder
    def read_from_traj(self,file: str):

        # ARC format trajectory
        if file.endswith(".arc") or '.arc' in file:
            print(f"Reading Tinker trajectory from file: {file}. It may take a while...")
            
            all_atom_crds = []
            all_box_sizes = []
            all_box_angles = []
            n_atoms = None
            pbc = None

            with open(file, "r") as f:
                with tqdm(desc="Processing trajectory", unit="frame") as t:

                    # Determine the number of atoms and whether the trajectory contains PBC information
                    for frame_index, line in enumerate(f):
                        if frame_index == 0:
                            n_atoms = int(line.strip().split()[0])
                        elif frame_index == 1:
                            pbc = len(line.split()) == 6
                            line_loop = n_atoms + 2 if pbc else n_atoms + 1
                        elif frame_index == 3:
                            break

                    f.seek(0)  # Reset the file pointer to the beginning of the file
                    
                    # PBC trajectory
                    if pbc:
                        for frame_index, line in enumerate(f):
                            if frame_index % line_loop == 0:
                                if frame_index != 0:  # Append data at the start of the new frame, after processing the previous frame
                                    all_atom_crds.append(np.array(atom_crds, dtype=float))
                                    all_box_sizes.append(box_size)
                                    all_box_angles.append(box_angle)
                                t.update()  # Updating the progress bar after processing each frame
                                atom_crds = []  # Reset for the new frame

                            elif frame_index % line_loop == 1:
                                box_params = np.fromstring(line, sep=' ')
                                box_size = box_params[:3]
                                box_angle = box_params[3:]

                            else:
                                crd = line.split()[2:5]
                                atom_crds.append(crd)
                        # Append the last frame after finishing the loop
                        all_atom_crds.append(np.array(atom_crds, dtype=float))
                        all_box_sizes.append(box_size)
                        all_box_angles.append(box_angle)

                    # Non-PBC trajectory
                    else:
                        for frame_index, line in enumerate(f):
                            if frame_index % line_loop == 0:
                                if frame_index != 0:  # Append data at the start of the new frame, after processing the previous frame
                                    all_atom_crds.append(np.array(atom_crds, dtype=float))
                                t.update()
                                atom_crds = []  # Reset for the new frame

                            else:
                                crd = line.split()[2:5]
                                atom_crds.append(crd)


                        # Append the last frame after finishing the loop
                        all_atom_crds.append(np.array(atom_crds, dtype=float))

                    self.AtomCrds = np.array(all_atom_crds)
                    self.BoxSize = np.array(all_box_sizes)
                    self.BoxAngle = np.array(all_box_angles)

            print(f"Successfully loaded {len(self.AtomCrds)} frames with {n_atoms} atoms each.")

        # DCD format trajectory
        elif file.endswith(".dcd") or '.dcd' in file:

            from MDAnalysis.lib.formats.libdcd import DCDFile

            # To store all frames' coordinates
            frames_xyz = []
            frames_box_size = []
            frames_box_angle = []

            # 读取 DCD 文件
            with DCDFile(file) as f:
                for frame in f:

                    frames_xyz.append(frame.xyz)
                    uc = frame.unitcell
                    
                    # box_size
                    box_size = np.array([uc[0], uc[2], uc[5]])
                    frames_box_size.append(box_size)
                    
                    # box_angle：
                    box_angle = np.array([90 - uc[1], 90 - uc[3], 90 - uc[4]])
                    frames_box_angle.append(box_angle)

            # Convert the list to numpy array
            all_frames = np.array(frames_xyz)       # shape: (n_frame, n_atom, 3)
            box_size = np.array(frames_box_size)      # shape: (n_frame, 3)
            box_angle = np.array(frames_box_angle)    # shape: (n_frame, 3)

            self.AtomCrds = np.array(all_frames)
            self.BoxSize = np.array(box_size)
            self.BoxAngle = np.array(box_angle)

            print(self.AtomCrds)
                    
            print(f"Successfully loaded {len(self.AtomCrds)} frames with {self.AtomNums} atoms each.")



if __name__ == '__main__':
        tktraj = TKMTrajectory()
        tktraj.read_from_tinker(r'/home/wayne/quanmol/TinkerModellor/example/rmsd/pr_coord.xyz')
        tktraj.read_from_traj(r'/home/wayne/quanmol/TinkerModellor/example/rmsd/pr_coord.arc')