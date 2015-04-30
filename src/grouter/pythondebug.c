//#include "Python.h"
#include "pythondebug.h"

int PythonError(PyObject *pObj)
{
    char *Str = PyString_AsString(pObj);
    return printf("%s", Str);
}

void CheckPythonError(void)
{
    if (PyErr_Occurred() != NULL)
    {
        PyErr_Print();
        PyErr_Clear();
    }
}
