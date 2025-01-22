#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <math.h>

#include <stdlib.h>
#include <stdbool.h>

PyObject* pdf(PyObject*, PyObject*);
PyObject* cdf(PyObject*, PyObject*);
PyObject* invcdf(PyObject*, PyObject*);

#ifndef NORMIE_PI
#define NORMIE_PI 3.14159265358979323846
#define RECI_SQRT_2_PI 0.3989422917366028
#endif


