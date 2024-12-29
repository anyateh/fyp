/**
 * Reference: https://docs.python.org/3/extending/embedding.html
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

int main(int argc, char** argv) {
	PyStatus status;
	PyConfig config;
	PyConfig_InitPythonConfig(&config);

	status = PyConfig_SetBytesString(&config, &config.program_name, argv[0]);
	if (PyStatus_Exception(status)) {
		PyConfig_Clear(&config);
		Py_ExitStatusException(status);
		return 1;
	}

	status = Py_InitializeFromConfig(&config);
	if (PyStatus_Exception(status)) {
		PyConfig_Clear(&config);
		Py_ExitStatusException(status);
		return 1;
	}
	PyConfig_Clear(&config);

	PyRun_SimpleString(
		"from time import time, ctime\n"
		"print('Today is', ctime(time()))\n"
		);
	
	if (Py_FinalizeEx() < 0) {
		exit(120);
	}
	return 0;
}
