#!/usr/bin/env python
import statsd
import time
import os
import socket
import sys
import yaml
import logging
import copy


config_file = "config.yml"


config = yaml.load(file(sys.path[0] + "/" + config_file))

prefix = config['namespace_prefix']
server = config['statsd_host']
port   = config['statsd_port']
update_interval = config['update_interval']

logger = logging.getLogger(config['app_name'])
hdlr = logging.FileHandler(config['logfile'])
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

# TODO:
# add argument parser for manual/on-the-fly usage

# debug output of the config file
#print(yaml.dump(config))

statsd_client = statsd.StatsClient(server, port, prefix = prefix)


while True:
	# prevent config['plugins'] from changing
	plugin_list = copy.deepcopy(config['plugins'])
	if config['stdout'] is True:
		print ("---------- " + time.strftime("%Y-%m-%d %H:%M:%S") + " ----------") 

	for plugin in plugin_list:

		# set namespace if given, if not set pluginname as namespace
		# TODO: double namespace detection
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
			# TEST:
			# does yaml ordering work with multile function parameters?
			results = imported_plugin.collect(**plugin)

			for name, value in results.items():
				full_namespace = namespace + "." + str(name)

				if config['stdout'] is True:
					print full_namespace, value 

				#FIXME: add different metric types to plugins, not only gauges
				statsd_client.gauge(full_namespace, value)
		except:
			#FIXME: handle Exceptions properly
			logger.error('command: "plugins/' + pluginname + '.py '+ str(plugin)+ '"failed! run the plugin directly to debug.')
	
	time.sleep(update_interval)
	
