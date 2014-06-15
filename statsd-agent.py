import statsd
import time
import psutil
import os
import socket

host = socket.gethostname()
server = '1.1.1.1'  #Define remote statsd server here
port = 8125         #Define remote port here

last_net_io   = psutil.net_io_counters()
net_speed = {}
statsd_client = statsd.StatsClient(server, port, prefix=host+'.')
while True:
    memory          = psutil.phymem_usage()
    disk            = psutil.disk_usage("/")
    net_io          = psutil.net_io_counters()
    net_speed['recv'] = (net_io.bytes_recv - last_net_io.bytes_recv) / 10
    net_speed['sent'] = (net_io.bytes_sent - last_net_io.bytes_sent) / 10
    last_net_io     = net_io
            
    gauges = {
        "memory.used":        memory.used,
        "memory.free":        memory.free,
        "memory.percent":     memory.percent,
        "cpu.percent":        psutil.cpu_percent(),
        "load":               os.getloadavg()[0],
        "disk.size.used":     disk.used,
        "disk.size.free":     disk.free,
        "disk.size.percent":  disk.percent,
        "net.in.bytes":       net_speed["recv"],
        "net.out.bytes":      net_speed["sent"],
        "net.in.errors":      net_io.errin,
        "net.in.dropped":     net_io.dropin,
        "net.out.errors":     net_io.errout,
        "net.out.dropped":    net_io.dropout,
    }
    
    for name, value in gauges.items():
        print name, value
        statsd_client.gauge(name, value)

    time.sleep(10)
