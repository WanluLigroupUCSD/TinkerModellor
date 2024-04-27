#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h> 
#include <eigen3/Eigen/Dense>
#include <cmath>
#include <iostream>
#include <vector>

namespace py = pybind11;

std::vector<double> angle(py::array_t<double> atom1, py::array_t<double> atom2, py::array_t<double> atom3) {
    py::buffer_info buf_atom1 = atom1.request(), buf_atom2 = atom2.request(), buf_atom3 = atom3.request();

    if (buf_atom1.shape[0] != buf_atom2.shape[0] || buf_atom2.shape[0] != buf_atom3.shape[0] ||
        buf_atom1.shape[1] != 3 || buf_atom2.shape[1] != 3 || buf_atom3.shape[1] != 3) {
        throw std::runtime_error("All input shapes must match and be of the form [n,3].");
    }

    int num_points = buf_atom1.shape[0];
    std::vector<double> angles;

    Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> coords1(
        static_cast<double*>(buf_atom1.ptr), num_points, 3);
    Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> coords2(
        static_cast<double*>(buf_atom2.ptr), num_points, 3);
    Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> coords3(
        static_cast<double*>(buf_atom3.ptr), num_points, 3);

    for (int i = 0; i < num_points; i++) {
        Eigen::Vector3d vec1 = coords1.row(i) - coords2.row(i);
        Eigen::Vector3d vec2 = coords3.row(i) - coords2.row(i);

        double cos_theta = vec1.dot(vec2) / (vec1.norm() * vec2.norm());
        double angle = std::acos(std::max(-1.0, std::min(1.0, cos_theta)));  // Clamp the value to avoid numerical errors
        angles.push_back(angle * (180.0 / M_PI));  // Convert from radians to degrees
    }

    return angles;
}

