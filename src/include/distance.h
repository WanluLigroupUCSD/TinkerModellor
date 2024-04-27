#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdexcept>

namespace py = pybind11;

std::vector<double> distance(py::array_t<double> atom1, py::array_t<double> atom2);