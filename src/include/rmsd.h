#ifndef RMSD_H
#define RMSD_H

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdexcept>

namespace py = pybind11;

std::vector<double> rmsd(py::array_t<double> ref_frame, py::array_t<double> traj_frames);

#endif // RMSD_H
