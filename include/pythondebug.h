/* 
 * File:   pythondebug.h
 * Author: chi
 *
 * Created on April 30, 2015, 5:13 PM
 */

#ifndef PYTHONDEBUG_H
#define	PYTHONDEBUG_H

#ifdef	__cplusplus
extern "C" {
#endif

#include "Python.h"

int PythonError(PyObject *pObj);
void CheckPythonError(void);

#ifdef	__cplusplus
}
#endif

#endif	/* PYTHONDEBUG_H */

