#!/usr/bin/env python
import statsd
import time
import os
import socket
import sys
import yaml
import logging


config_file = "config.yml"


config = yaml.load(file(sys.path[0] + "/" + config_file))

prefix = config['namespace_prefix']
server = config['statsd_host']
port   = config['statsd_port']

logger = logging.getLogger(config['app_name'])
hdlr = logging.FileHandler(config['logfile'])
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)


#debugging of the config file
#print(yaml.dump(config))

statsd_client = statsd.StatsClient(server, port, prefix = prefix)

for plugin in config['plugins']:
	if 'namespace' in plugin: 
	    namespace = plugin['namespace']
	    del plugin['namespace']
	else:
	    namespace = plugin['plugin']

	pluginname = plugin['plugin']

	# remove the plugin name from the dict
	del plugin['plugin']


	try:
		imported_plugin = __import__("plugins.%s" % pluginname, fromlist=["plugins"])
	except ImportError:
		logger.error("error importing " + pluginname + ".py!")
	
	# pass the remaining dict items as method parameters
	try:
		results = imported_plugin.collect(**plugin)
		for name, value in results.items():
			full_namespace = namespace + "." + str(name)
			print full_namespace, value
			
			#FIXME: add different data types to plugins
			statsd_client.gauge(name, value)
	except:
		#print plugin
		logger.error('command: "plugins/' + pluginname + '.py '+ str(plugin)+ '"failed! run the plugin directly to debug.')





#while True:
#    
#    statsd_client.gauge(name, value)
#
#    time.sleep(10)
