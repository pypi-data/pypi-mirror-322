#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <math.h>

#include <stdlib.h>
#include <stdbool.h>

#include "normie.h"


static PyMethodDef NormieImplMethods[] =
{
     {"pdf", pdf, METH_VARARGS, "Normal probability density function"},
     {"cdf", cdf, METH_VARARGS, "Normal cumulative distribution function"},
     {"invcdf", invcdf, METH_VARARGS, "Normal inverse cumulative distribution function"},
     {NULL, NULL, 0, NULL}
};

struct module_state {
	PyObject *error;
};

static int normie_impl_traverse(PyObject *m, visitproc visit, void *arg) {
	Py_VISIT(((struct module_state*)PyModule_GetState(m))->error);
	return 0;
}

static int normie_impl_clear(PyObject *m) {
	Py_CLEAR(((struct module_state*)PyModule_GetState(m))->error);
	return 0;
}

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	"normie_impl",
	NULL,
	sizeof(struct module_state),
	NormieImplMethods,
	NULL,
	normie_impl_traverse,
	normie_impl_clear,
	NULL
};


/* module initialization */
PyMODINIT_FUNC
PyInit_normie_impl(void)
{
     PyObject *module = PyModule_Create(&moduledef);

     if (module == NULL)
	 return NULL;

     struct module_state *st = (struct module_state*)PyModule_GetState(module);
     // ??
     st->error = PyErr_NewException("exact_cover.Error", NULL, NULL);
     if (st->error == NULL) {
	     Py_DECREF(module);
	     return NULL;
     }

     return module;
}


