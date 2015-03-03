#!/usr/bin/env python

def collect():
    import psutil
    memory = psutil.phymem_usage()

    gauges = {
        "used":        memory.used,
        "free":        memory.free,
        "total":       memory.total,
    }
    return gauges


if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='retrieve system memory')
    args = parser.parse_args()
    output = collect()
    for name, value in output.items():
        print name, value
