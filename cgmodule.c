#include "Python.h"

/* Function of two integers returning integer */

PyDoc_STRVAR(cg_scan_doc,
"scan(i,j)\n\
\n\
Return the sum of i and j.");

#define BUFSIZE (2 * 1024 * 1024)
static char buf[BUFSIZE];

#define ARRAY_DIMENSION   (176 - 32)
#define ARRAYSIZE  (ARRAY_DIMENSION * ARRAY_DIMENSION * ARRAY_DIMENSION)
static char array[ARRAYSIZE];

static PyObject *
cg_scan(PyObject *self, PyObject *args)
{
    PyObject *d0, *d, *d1, *Fi, *pkey0, *pkey1;
    char *filename;
    unsigned char ok, x;
    long i, fi, n;
    FILE *f;
    char key0[2], key1[3];
    if (!PyArg_ParseTuple(args, "Ols:scan", &d0, &fi, &filename))
        return NULL;
    Fi = PyInt_FromLong(fi);
    key0[1] = key1[2] = '\0';
    f = fopen(filename, "r");
    n = fread(buf, 1, BUFSIZE, f);
    memset(array, 0, ARRAYSIZE);
    if (n > 2) {
        for (i = 0, ok = 1; i < n; i++) {
            x = (int) buf[i];
            if (x > 176) {
                ok = 0;
                break;
            }
            if (x >= 32) {
                continue;
            }
            if (x == '\x0C' || x == '\r' || x == '\n' || x == '\t') {
                continue;
            }
            ok = 0;
            break;
        }
        if (ok) {
            for (i = 0; i < n - 2; i++) {
                key0[0] = buf[i];
                pkey0 = PyString_FromString(key0);
                if (!PyDict_Contains(d0, pkey0)) {
                    d = PyDict_New();
                    PyDict_SetItem(d0, pkey0, d);
                    Py_DECREF(d);
                }
                d = PyDict_GetItem(d0, pkey0);

                key1[0] = buf[i+1];
                key1[1] = buf[i+2];
                pkey1 = PyString_FromString(key1);
                if (!PyDict_Contains(d, pkey1)) {
                    d1 = PyDict_New();
                    PyDict_SetItem(d, pkey1, d1);
                    Py_DECREF(d1);
                }
                d1 = PyDict_GetItem(d, pkey1);
                PyDict_SetItem(d1, Fi, Py_None);
                Py_DECREF(pkey1);
                Py_DECREF(pkey0);
            }
        }
    }
    fclose(f);
    Py_DECREF(Fi);
    Py_INCREF(Py_None);
    return Py_None;
}


/* ---------- */


/* List of functions defined in the module */

static PyMethodDef cg_methods[] = {
    {"scan",             cg_scan,         METH_VARARGS,
        cg_scan_doc},
    {NULL,              NULL}           /* sentinel */
};

PyDoc_STRVAR(module_doc,
"This is a template module just for instruction.");

/* Initialization function for the module (*must* be called initcg) */

PyMODINIT_FUNC
initcg(void)
{
    Py_InitModule3("cg", cg_methods, module_doc);
}
