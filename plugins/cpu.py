#!/usr/bin/env python
import statsd
import time
import psutil
import os
import socket
import sys
import yaml

            
gauges = {
    "cpu.percent":        psutil.cpu_percent(),
    "load":               os.getloadavg()[0],
}
    
for name, value in gauges.items():
    print name, value

