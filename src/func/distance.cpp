#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h> 
#include <eigen3/Eigen/Dense>
#include <iostream>
#include <vector>

namespace py = pybind11;

std::vector<double> distance(py::array_t<double> atom1, py::array_t<double> atom2) {
    py::buffer_info buf_atom1 = atom1.request(), buf_atom2 = atom2.request();

    if (buf_atom1.shape[0] != buf_atom2.shape[0] || buf_atom1.shape[1] != 3 || buf_atom2.shape[1] != 3) {
        throw std::runtime_error("Input shapes must match and be of the form [n,3] for both trajectories.");
    }

    int num_points = buf_atom1.shape[0];
    std::vector<double> distances;

    Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> coords1(
        static_cast<double*>(buf_atom1.ptr), num_points, 3);
    Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> coords2(
        static_cast<double*>(buf_atom2.ptr), num_points, 3);

    for (int i = 0; i < num_points; i++) {
        distances.push_back((coords1.row(i) - coords2.row(i)).norm());
    }

    return distances;
}
