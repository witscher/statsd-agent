#!/usr/bin/env python
import statsd
import time
import psutil
import os
import socket
import sys
import yaml

config_path = "config.yml"

config = yaml.load(file(config_path))

prefix = config['namespace_prefix']
server = config['statsd_host']
port   = config['statsd_port']

last_net  = psutil.net_io_counters()
net_speed = {}

statsd_client = statsd.StatsClient(server, port, prefix = prefix)

while True:
    memory = psutil.phymem_usage()
    disk   = psutil.disk_usage("/")

    net    = psutil.net_io_counters()
    net_speed['recv'] = (net.bytes_recv - last_net.bytes_recv) / 10
    net_speed['sent'] = (net.bytes_sent - last_net.bytes_sent) / 10
    last_net = net

    gauges = {
        "memory.used":        memory.used,
        "memory.free":        memory.free,
        "memory.total":       memory.total,
        "cpu.percent":        psutil.cpu_percent(),
        "load":               os.getloadavg()[0],
        "disk.size.used":     disk.used,
        "disk.size.total":     disk.total,
        "net.in.bytes":       net_speed["recv"],
        "net.out.bytes":      net_speed["sent"],
        "net.in.errors":      net.errin,
        "net.in.dropped":     net.dropin,
        "net.out.errors":     net.errout,
        "net.out.dropped":    net.dropout,
    }

    for name, value in gauges.items():
        print name, value
        statsd_client.gauge(name, value)

    time.sleep(10)
