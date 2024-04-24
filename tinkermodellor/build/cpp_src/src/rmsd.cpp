#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <eigen3/Eigen/Dense>
#include <iostream>

namespace py = pybind11;

double rmsd(py::array_t<py::array_t<double>> arr1, py::array_t<py::array_t<>double> arr2) {
    py::buffer_info buf1 = arr1.request(), buf2 = arr2.request();

    if (buf1.shape[0] != buf2.shape[0] || buf1.shape[1] != 3 || buf2.shape[1] != 3) {
        throw std::runtime_error("Input shapes must be [n,3]");
    }

    int num_atoms = buf1.shape[0];
    Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> mat1(static_cast<double*>(buf1.ptr), num_atoms, 3);
    Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> mat2(static_cast<double*>(buf2.ptr), num_atoms, 3);

    Eigen::Matrix<double, Eigen::Dynamic, 1> diff = (mat1 - mat2).colwise().squaredNorm().array().sqrt();
    double rmsd = std::sqrt(diff.squaredNorm() / num_atoms);
    return rmsd;
}

PYBIND11_MODULE(tkmtoolkit, m) {
    m.def("rmsd", &rmsd, "A function to compute the RMSD between two sets of atomic coordinates.");
}
