import numpy as np
import os
import sys
import pandas as pd
from tqdm import tqdm
from typing import List, Union, Tuple
from ._tinkersystemcharge import TinkerSystemCharge
#from tinkermodellor.build.function.ef_calculation._tinkersystemcharge import TinkerSystemCharge
from ...system.tinker._tkmtrajectory import TKMTrajectory

from ....messager import TKMEFPointReminder, TKMEFBondReminder, TKMEFGridReminder


class ElectricFieldComputeTraj():

    def __init__(self,charge_method: str = None, tinker_xyz: str = None, tinker_arc: str = None):
        """
            This class is used to compute electric field at a point or along a bond
            Args:
                charge_method: Charge method to be used to compute charges
                tinker_xyz: Tinker xyz file path
                tinker_arc: Tinker arc file path
        """
        self.units = 1.602 # Conversion factor to MV/cm
        # Constant k = 1 / (4 * pi * epsilon_0)
        self.k = 8.9875517873681764e2  # N m²/C² (Coulomb's constant)

        if charge_method is None:
            print("No charge method specified, using default charge method: eem")
            self.charge_method = 'eem'
        elif charge_method not in ['eem', 'qeq', 'qtpie', 'eqeq']:
            raise NotImplementedError(f"Charge method {charge_method} not implemented")
        else:
            self.charge_method = charge_method

        if tinker_xyz is None:
            raise ValueError("No tinker xyz file specified")
        if isinstance(tinker_xyz, str):
            tinker_xyz = os.path.abspath(tinker_xyz)

        self.tinker_system_charged = TinkerSystemCharge(self.charge_method)
        self.tinker_system_charged(tinker_xyz)
        self.charge = self.tinker_system_charged.Charges

        self.tinker_traj = TKMTrajectory()
        self.tinker_traj.read_from_tinker(tinker_xyz)
        self.tinker_traj.read_from_traj(tinker_arc)

    @TKMEFPointReminder
    def compute_point_ef_traj(self, point: Union[np.array, List], output: str = None) -> List[List[float]]:
        """
        This function is used to compute the electric field at a point.
        
        Args:
            point: Point at which the electric field is to be computed.
            output: Path to save the output CSV file. If None, saves to the current directory.
            
        Returns:
            results: Electric field at the point, including the magnitude.
                            Format is [E_x, E_y, E_z, |E|].

        """
        # Convert point to a numpy 3D array if it's not already
        point = [float(i) for i in point]
        point = np.array(point, dtype=float).reshape(3)

        results = []
        for i in range(len(self.tinker_traj.AtomCrds)):
            coordinates = self.tinker_traj.AtomCrds[i]
            results.append(self._compute_point_ef(point, coordinates, self.charge))
        
        print("Electric field at the point has been successfully computed")
        
        # Create a DataFrame to store the results
        df = pd.DataFrame(results, columns=['E_x', 'E_y', 'E_z', '|E|'])
        df.insert(0, 'frame', range(1, len(df) + 1))
        
        # Determine the output path
        if output is None:
            output = os.path.join(os.getcwd(), 'point_ef.csv')
        else:
            output = os.path.abspath(output)
        
        # Save the DataFrame to a CSV file
        df.to_csv(output, index=False)
        
        print(f"Results have been saved to {output}")
        
        return results

    def _compute_point_ef(self,point: Union[np.array, List],coordinates:np.array,charges:np.array) -> List[float]:
        """
        This function is used to compute the electric field at a point.
        
        Args:
            point: Point at which the electric field is to be computed.
            coordinates: Coordinates of the atoms in the system.
            charges: Charges of the atoms in the system.
            
        Returns:
            electric_field: Electric field at the point, including the magnitude.
                            Format is [E_x, E_y, E_z, |E|].
        """

        # Initialize electric field
        electric_field = np.zeros(3)

        # Compute the electric field
        for charge, coord in zip(charges, coordinates):
            # Calculate the vector from the charge to the point
            r_vector = point - coord

            # Calculate the distance
            r_magnitude = np.linalg.norm(r_vector)

            # Skip calculation if distance is zero to avoid division by zero
            if r_magnitude == 0:
                continue

            # Calculate the electric field contribution from this charge
            e_field_contribution = self.k * charge * r_vector / r_magnitude**3

            # Add the contribution to the total electric field
            electric_field += e_field_contribution

        # Convert electric field to MV/cm
        electric_field *= self.units
        # Calculate the magnitude of the electric field
        e_magnitude = np.linalg.norm(electric_field)

        # Create a 1*4 array containing the electric field components and its magnitude
        result = np.append(electric_field, e_magnitude)

        return result
    
    @TKMEFBondReminder
    def compute_bond_ef_traj(self, bond: List[int], output: str = None, \
                            mask:bool = True, on_the_fly: bool=False) -> List[List[float]]:
        """
        This function is used to compute the electric field at a point.
        
        Args:
            point: Point at which the electric field is to be computed.
            output_path: Path to save the output CSV file. If None, saves to the current directory.
            mask: Whether to mask the electric field contribution of the molecules, which are not part of the bond.
            on_the_fly: Whether to compute the charges on-the-fly. Default is False.

        Returns:
            results: Electric field at the point, including the magnitude.
                            Format is [E_x, E_y, E_z, |E|].

        """
        # Check if bond length is 2
        if len(bond) != 2:
            raise ValueError("Bond must define exactly two atoms.")
        
        # Extract atom indices
        atom1_idx, atom2_idx = bond
        zero_based_ndx = [atom1_idx-1, atom2_idx-1]

        results = []

        mask_atom = self._connectivity_search(bond, self.tinker_traj.Bonds)
        
        for i in tqdm(range(len(self.tinker_traj.AtomCrds)), desc="Calculating Electric Field"):
            coordinates = self.tinker_traj.AtomCrds[i]
            if on_the_fly:
                self.tinker_system_charged.update_charge(coordinates)
                self.charge = self.tinker_system_charged.Charges
            
            atomcrd1 = self.tinker_traj.AtomCrds[i][atom1_idx-1]
            atomcrd2 = self.tinker_traj.AtomCrds[i][atom2_idx-1]
            if mask:
                coordinates, charges = self._mask(mask_atom, coordinates, self.charge)
            else:
                charges = self.charge
            
            results.append(self._compute_bond_ef(atomcrd1, atomcrd2, coordinates, charges))

        print(f"Electric field projected onto the bond has been successfully computed across {len(self.tinker_traj.AtomCrds)} frames with {self.tinker_traj.AtomNums} atoms each.")
        
        # Create a DataFrame to store the results
        df = pd.DataFrame(results, columns=['ElectricField'])
        df.insert(0, 'frame', range(1, len(df) + 1))
        
        # Determine the output path
        if output is None:
            output = os.path.join(os.getcwd(), 'bond_ef.csv')
        else:
            output = os.path.abspath(output)
        
        # Save the DataFrame to a CSV file
        df.to_csv(output, index=False)

        print(f"Results have been saved to {output}")
        
        return results

    def _compute_bond_ef(self, atomcrd1:np.array, atomcrd2:np.array,coordinates:np.array,charges) -> float:
        """
        This function computes the average electric field along a bond defined by two atoms.

        Args:
            atomcrd1: Coordinates of the first atom.
            atomcrd2: Coordinates of the second atom.
            coordinates: Coordinates of the atoms in the system.
            charges: Charges of the atoms in the system.

        Returns:
            bond_electric_field: Electric field projected along the bond.
        """

        # Get coordinates of the two atoms
        # The index in the Tinker system is 0-based

        # Calculate the bond vector and normalize it to get the unit vector
        bond_vector = atomcrd2 - atomcrd1
        bond_unit_vector = bond_vector / np.linalg.norm(bond_vector)

        # Calculate electric fields at the two atom positions
        ef_atom1 = self._compute_point_ef(atomcrd1,coordinates,charges)[:3]  # Extract E_x, E_y, E_z
        ef_atom2 = self._compute_point_ef(atomcrd2,coordinates,charges)[:3]  # Extract E_x, E_y, E_z

        # Calculate the average electric field
        avg_ef = (ef_atom1 + ef_atom2) / 2

        # Project the average electric field onto the bond's unit vector
        projection = np.dot(avg_ef, bond_unit_vector)

        # Result is the projection of the average electric field onto the bond direction
        return projection

    @TKMEFGridReminder
    def compute_grid_ef_traj(self,point: Union[np.array, List[float]], radius: float, 
                        density_level: int, if_output: bool = True, output_prefix: str = 'TKM') -> List[List[float]]:
        """
        Compute the electric field at grid points around a central point.

        Args:
            point: The coordinates of the central point.
            tinker_system_charged: Tinker system with charges assigned.
            radius: The radius for the grid expansion around the central point.
            density_level: Density level of the grid points (1 for 5 points, 2 for 10 points, 3 for 20 points).
            if_output: Whether to output the DX files for the electric field components and magnitude.
            output_prefix: The prefix for the output DX files.
            
        Returns:
            results: List of electric field results at each grid point.
                    Each element is [x, y, z, E_x, E_y, E_z, |E|].
        """

        raise NotImplementedError("This function is not implemented yet")

        # Convert the point to a numpy 3D array
        if not isinstance(point, (list, tuple, np.ndarray)):
            raise TypeError("Point must be a list, tuple, or numpy array.")
        if len(point) != 3:
            raise ValueError("Point must have exactly 3 coordinates: [x, y, z].")

        # Convert the point to a numpy 3D array
        point = np.array(point, dtype=float).reshape(3)

        # Define a mapping from density level to the number of points per axis
        density_map = {1: 5, 2: 10, 3: 20, 4:50, 5:100}
        num_points_per_axis = density_map.get(density_level, 20) 

        # Calculate the step size
        step = 2 * radius / (num_points_per_axis - 1)

        # Create a grid centered around the central point
        grid_points = []
        for i in range(num_points_per_axis):
            for j in range(num_points_per_axis):
                for k in range(num_points_per_axis):
                    # Calculate the current grid point's coordinates
                    x = point[0] - radius + i * step
                    y = point[1] - radius + j * step
                    z = point[2] - radius + k * step
                    grid_points.append([x, y, z])

        # Extract charges and coordinates from tinker_system_charged
        charges = self.tinker_system_charged.Charges
        coordinates = self.tinker_system_charged.AtomCrds

        # Constant k = 1 / (4 * pi * epsilon_0)
        k = 8.9875517873681764e9  # N m²/C² (Coulomb's constant)

        # Store the electric field results for all grid points
        results = []

        # Compute the electric field at each grid point
        for grid_point in grid_points:
            electric_field = np.zeros(3)

            for charge, coord in zip(charges, coordinates):
                # Calculate the vector from the charge to the grid point
                r_vector = np.array(grid_point) - coord

                # Calculate the distance
                r_magnitude = np.linalg.norm(r_vector)

                # Avoid division by zero
                if r_magnitude == 0:
                    continue

                # Calculate the electric field contribution from this charge
                e_field_contribution = k * charge * r_vector / r_magnitude**3

                # Add the contribution to the total electric field
                electric_field += e_field_contribution

            # Convert electric field to MV/cm
            electric_field *= self.units

            # Calculate the magnitude of the electric field
            e_magnitude = np.linalg.norm(electric_field)

            # Store the result as [x, y, z, E_x, E_y, E_z, |E|]
            result = list(grid_point) + list(electric_field) + [e_magnitude]
            results.append(result)
        
        if if_output:
            self._generate_grid_output(results, point, radius, density_level, output_prefix)

        return results
    
    def _generate_grid_output(self, results: List[List[float]], origin: List[float], radius: float, density_level: int, output_prefix: str):
        """
        Generate DX files for electric field components and magnitude from the grid results.

        Args:
            results: List of electric field results at each grid point.
                    Each element is [x, y, z, E_x, E_y, E_z, |E|].
            origin: The origin point of the grid.
            radius: The radius of the grid expansion around the central point.
            density_level: Density level of the grid points (1 for 5 points, 2 for 11 points, 3 for 21 points).
            output_prefix: The prefix for the output DX files.
        """
        # Define a mapping from density level to the number of points per A
        density_map = {1: 5, 2: 10, 3: 20, 4:50, 5:100}
        num_points_per_axis = density_map.get(density_level, 20) 

        # Calculate the step size
        step = 2 * radius / (num_points_per_axis - 1)

        # Number of grid points
        num_points = num_points_per_axis**3

        # Helper function to write a DX file
        def write_dx_file(filename: str, data: np.ndarray):
            with open(filename, 'w') as f:
                f.write(f"object 1 class gridpositions counts {num_points_per_axis} {num_points_per_axis} {num_points_per_axis}\n")
                f.write(f"origin {origin[0]-radius} {origin[1]-radius} {origin[2]-radius}\n")
                f.write(f"delta {step} 0 0\n")
                f.write(f"delta 0 {step} 0\n")
                f.write(f"delta 0 0 {step}\n")
                f.write(f"object 2 class gridconnections counts {num_points_per_axis} {num_points_per_axis} {num_points_per_axis}\n")
                f.write(f"object 3 class array type double rank 0 items {num_points} data follows\n")

                # Write the data points
                line_count = 0
                for value in data:
                    f.write(f"{value:.6e} ")
                    line_count += 1
                    if line_count == 3:
                        f.write("\n")
                        line_count = 0

                if line_count != 0:
                    f.write("\n")

                f.write('attribute "dep" string "positions"\n')

        # Extract each component and magnitude into separate arrays
        ex = np.array([result[3] for result in results])
        ey = np.array([result[4] for result in results])
        ez = np.array([result[5] for result in results])
        magnitude = np.array([result[6] for result in results])

        # Write each component to a separate DX file
        write_dx_file(f"{output_prefix}_Ex.dx", ex)
        write_dx_file(f"{output_prefix}_Ey.dx", ey)
        write_dx_file(f"{output_prefix}_Ez.dx", ez)
        write_dx_file(f"{output_prefix}_Magnitude.dx", magnitude)

        print(f"DX files have been successfully saved with prefix {output_prefix}")



    def _mask(self, mask_ndx: List[int], coordinates: np.array, charges: np.array) -> Tuple[np.array, np.array]:
        """
        This function is used to mask specific molecules in the system according to the atom indices, and 
        then neglect the electric field contribution from the masked atoms.

        Args:
            mask_ndx: Atom indices to be masked.
            coordinates: Coordinates of the atoms in the system.
            charges: Charges of the atoms in the system.

        Returns:
            Tuple containing the new coordinates and charges after masking.
        """
        # Convert mask_ndx to a set for efficient lookup
        mask_set = set(mask_ndx)
        
        # Filter out the coordinates and charges corresponding to the masked indices
        # The index in the Tinker system is 1-based so we need to adjust for 0-based indexing (i+1)
        new_coordinates = np.array([coord for i, coord in enumerate(coordinates) if i+1 not in mask_set])
        new_charges = np.array([charge for i, charge in enumerate(charges) if i+1 not in mask_set])
        
        return new_coordinates, new_charges


    def _connectivity_search(self,ndx: List, bonds) -> List[int]:
        """
        Finds all atoms connected to the initial atom index, ensuring entire molecules or connected components are marked.

        Args:
            initial (int): Initial atom index to start the search.

        Returns:
            List[int]: Complete list of connected atom indices, sorted.
        """

        atom_in_molecule = []
        for initial in ndx:
            # Ensure the initial atom index is valid
            if initial < 1 or initial > len(bonds):
                raise ValueError(f"Initial atom index {initial} is out of bounds.")

            sys.setrecursionlimit(10000)
            residue_list = []
            visited = set()  # Track visited atoms to prevent infinite recursion

            def explore_bonded_atoms(atom_index):
                """Recursively adds bonded atoms to the list."""
                if atom_index in visited:
                    return
                visited.add(atom_index)
                residue_list.append(atom_index)

                for bonded_atom in bonds[atom_index - 1]:  # Adjust for 0-indexing
                    explore_bonded_atoms(bonded_atom)

                

            explore_bonded_atoms(initial)

            # Sort residue_list with the largest number first
            residue_list = sorted(residue_list, reverse=True)

            # Add to atom_in_molecule if not already included
            atom_in_molecule.extend(residue_list)

        # Remove duplicates and sort atom_in_molecule with the largest number first
        atom_in_molecule = sorted(set(atom_in_molecule), reverse=True)

        return atom_in_molecule
