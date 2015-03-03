#!/usr/bin/env python


def collect():
    import psutil
    import os

    load = os.getloadavg()

    gauges = {
        "cpu.percent":        psutil.cpu_percent(),
        "load1":               load[0],
        "load5":               load[1],
        "load15":              load[2],
    }


    d = psutil.cpu_times_percent(percpu=True)
    cpu = 0


    for item in d:
        cpu_no = "cpu" + str(cpu)
        gauges[ cpu_no + ".user"] = item.user
        gauges[ cpu_no + ".system"] = item.system
        gauges[ cpu_no + ".idle"] = item.idle
        gauges[ cpu_no + ".nice"] = item.nice
        gauges[ cpu_no + ".iowait"] = item.iowait
        gauges[ cpu_no + ".irq"] = item.irq
        gauges[ cpu_no + ".softirq"] = item.softirq
        gauges[ cpu_no + ".steal"] = item.steal
        #gauges[ cpu_no + ".guest"] = item.guest
        #gauges[ cpu_no + ".guest_nice"] = item.guest_nice

        cpu += 1


    return gauges

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='retrieve cpu values')
    args = parser.parse_args()
    output = collect()
    for name, value in output.items():
        print name, value
