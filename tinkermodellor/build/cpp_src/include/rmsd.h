#ifndef RMSD_H
#define RMSD_H

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Eigen/Dense>
#include <stdexcept>
#include <rmsd.h>

namespace py = pybind11;

double compute_rmsd(py::array_t<double> arr1, py::array_t<double> arr2);

#endif // RMSD_H
