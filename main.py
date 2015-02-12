#!/usr/bin/env python
import statsd
import time
import psutil
import os
import socket
import sys
import yaml

config_file = "config.yml"

config = yaml.load(file(config_file))

prefix = config['namespace_prefix']
server = config['statsd_host']
port   = config['statsd_port']

#debugging of the config file
#print(yaml.dump(config))


for plugin in config['plugins']:
	#os.system("script2.py 1")
	if 'namespace' in plugin: 
	    namespace = plugin['namespace']
	    del plugin['namespace']
	else:
	    namespace = plugin['plugin']

	pluginname = plugin['plugin']

	del plugin['plugin']

	print(namespace + '.' +  pluginname + '.py')

	for name,value in plugin.items():
		print ('--' + str(name) + ' "' + str(value) + '"')


#statsd_client = statsd.StatsClient(server, port, prefix = prefix)

#while True:
#    
#    statsd_client.gauge(name, value)
#
#    time.sleep(10)
