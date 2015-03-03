#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-n', metavar='<interface name>', default=False, help='the name of the network interface - defaults to "all"')

args = parser.parse_args()

# CHristians zeugs:
# d = psutil.network_io_counters(pernic=True)
# k = d.keys()
# names = d.values()[0]._asdict().keys()
# print names

def collect():
    import time
    import psutil
    import os
    import sys

    last_net  = psutil.net_io_counters(pernic=True)
    net_speed = {}

    time.sleep(5)

    net    = psutil.net_io_counters(pernic=True)
    for nic, value in net.items():


        net_speed['recv'] = (net[nic].bytes_recv - last_net[nic].bytes_recv) / 5
        net_speed['sent'] = (net[nic].bytes_sent - last_net[nic].bytes_sent) / 5
        print net[nic].bytes_sent
        print net[nic].bytes_recv
        print last_net[nic].bytes_sent
        print last_net[nic].bytes_recv
        last_net = net

        print ("Netspeed =" + str(net_speed))


        gauges = {
            "net." + str(nic) + ".in.bytes":       net_speed["recv"],
            "net." + str(nic) + ".out.bytes":      net_speed["sent"],
            "net." + str(nic) + ".in.errors":      value.errin,
            "net." + str(nic) + ".in.dropped":     value.dropin,
            "net." + str(nic) + ".out.errors":     value.errout,
            "net." + str(nic) + ".out.dropped":    value.dropout,
        }
        net_speed = {}

        for name, value in gauges.items():
            print name, value



if __name__ == "__main__":
    import sys
    collect()
