#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <math.h>

#include <stdlib.h>
#include <stdbool.h>

#include "normie.h"


PyObject* pdf(PyObject* self, PyObject* args)
{
    double x;

    /*  Parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "d", &x)) return NULL;

    double z = exp(-x * x / 2.0) * RECI_SQRT_2_PI;
    return Py_BuildValue("d", z);
}


PyObject* cdf(PyObject* self, PyObject* args)
{
    double x;

    /*  Parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "d", &x)) return NULL;

    double z = erfc(-x / sqrt(2.0)) / 2.0;
    return Py_BuildValue("d", z);
}

/*
 *  Acklam's Algorithm
 *  https://stackedboxes.org/2017/05/01/acklams-normal-quantile-function/
 */

const double a[] = {
    -3.969683028665376e+01, 
    2.209460984245205e+02,
    -2.759285104469687e+02,
    1.383577518672690e+02,
    -3.066479806614716e+01,
    2.506628277459239e+00
};

const double b[] = {
    -5.447609879822406e+01,
    1.615858368580409e+02,
    -1.556989798598866e+02,
    6.680131188771972e+01,
    -1.328068155288572e+01
};

const double c[] = {
    -7.784894002430293e-03,
    -3.223964580411365e-01,
    -2.400758277161838e+00,
    -2.549732539343734e+00,
     4.374664141464968e+00,
     2.938163982698783e+00
};

const double d[] = {
    7.784695709041462e-03,
    3.224671290700398e-01,
    2.445134137142996e+00,
    3.754408661907416e+00
};

PyObject* invcdf(PyObject* self, PyObject* args)
{
    double x, q, r, z;
    double p_low = 0.02425;

    /*  Parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "d", &x)) return NULL;

    if (x == 0.0){
        return Py_BuildValue("d", -INFINITY);
    }

    if (x == 1.0){
        return Py_BuildValue("d", INFINITY);
    }

    if (x < p_low)
    {
        q = sqrt(-2*log(x));
        z = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);

        return Py_BuildValue("d", z);
    }
    if (x > 1.0 - p_low)
    {
        q = sqrt(-2*log(1-x));
        z = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);

        return Py_BuildValue("d", z);
    }
    
    q = (x - 0.5);
    r = q * q;
    z = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);

    return Py_BuildValue("d", z);
}
