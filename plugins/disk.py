#!/usr/bin/env python

def collect(mountpoint="/"):
	import psutil

	
	disk   = psutil.disk_usage(mountpoint)


	gauges = {
	    "used":     disk.used,
	    "total":     disk.total,
	}
	    
	return gauges

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', metavar='<mount point>', default='/', help='which mountpoint to check')
    args = parser.parse_args()
    output = collect(args.d)
    for name, value in output.items():
    	print name, value
