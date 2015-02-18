#!/usr/bin/env python


def collect(procname = None):
	import psutil

	number = 0
	nomatch = False

	for proc in psutil.process_iter():
		if procname != None:
			if proc.name in str(procname):
				number += 1
				
		else:
			number += 1
			nomatch = True

	if nomatch:
		procname = "total"


	processes = { procname : number}

	return processes

if __name__ == "__main__":
    import sys
    output = collect()
    for name, value in output.items():
	    print name, value