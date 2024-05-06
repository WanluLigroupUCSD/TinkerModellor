#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "angle.h"
#include "distance.h"
#include "rmsd.h"

namespace py = pybind11;

PYBIND11_MODULE(tkmtoolkit, m) {
    m.def("rmsd", &rmsd, "A function to compute the RMSD between a reference frame and multiple trajectory frames.");
    m.def("distance", &distance, "A function to compute the distance between two atoms.");
    m.def("angle", &angle, "A function to compute angles formed by three atoms over time.");
}
/*

# rmsd
# This function computes the RMSD between a reference frame and multiple trajectory frames.
# Args:
#     ref_frame (np.ndarray): A 2D numpy array of shape (n_atoms, 3) representing the reference frame.
#     traj_frames (np.ndarray): A 3D numpy array of shape (n_frames, n_atoms, 3) representing the trajectory frames.
# Returns:
#     list: A list of RMSD values for each trajectory frame.

# distance
# This function computes the distance between two atoms.
# Args:
#     atom1 (np.ndarray): A 1D numpy array of shape (,3) representing the coordinates of atom1.
#     atom2 (np.ndarray): A 1D numpy array of shape (,3) representing the coordinates of atom2.
# Returns:
#     list: A list containing the distance between atom1 and atom2.

# angle
# This function computes the angle formed by three atoms over time.
# Args:
#     atom1 (np.ndarray): A 1D numpy array of shape (,3) representing the coordinates of atom1.
#     atom2 (np.ndarray): A 1D numpy array of shape (,3) representing the coordinates of atom2, this is the central atom for the angle calculation
#     atom3 (np.ndarray): A 1D numpy array of shape (,3) representing the coordinates of atom3.
# Returns:
#     list: A list of angles formed by the three atoms over time.

*/