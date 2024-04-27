#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h> 
#include <eigen3/Eigen/Dense>
#include <iostream>
#include <vector>

namespace py = pybind11;

std::vector<double> rmsd(py::array_t<double> ref_frame, py::array_t<double> traj_frames) {
    py::buffer_info buf_ref = ref_frame.request(), buf_traj = traj_frames.request();

    if (buf_ref.shape[0] != buf_traj.shape[1] || buf_ref.shape[1] != 3 || buf_traj.shape[2] != 3) {
        throw std::runtime_error("Input shapes must match and be of the form [n,3] for the reference and [m,n,3] for the trajectory.");
    }

    int num_frames = buf_traj.shape[0];
    int num_atoms = buf_ref.shape[0];

    Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> ref_mat(
        static_cast<double*>(buf_ref.ptr), num_atoms, 3);

    std::vector<double> rmsd_values;

    for (int i = 0; i < num_frames; i++) {
        Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> frame_mat(
            static_cast<double*>(buf_traj.ptr) + i * num_atoms * 3, num_atoms, 3);

        Eigen::Matrix<double, Eigen::Dynamic, 1> diff = (ref_mat - frame_mat).colwise().squaredNorm().array().sqrt();
        double rmsd = std::sqrt(diff.squaredNorm() / num_atoms);
        rmsd_values.push_back(rmsd);
    }

    return rmsd_values;
}