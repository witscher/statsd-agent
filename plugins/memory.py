#!/usr/bin/env python
import psutil

def collect():
	memory = psutil.phymem_usage()
            
	gauges = {
	    "used":        memory.used,
	    "free":        memory.free,
	    "total":       memory.total,
	}
	return gauges
	

if __name__ == "__main__":
    import sys
    output = collect()
    for name, value in output.items():
	    print name, value