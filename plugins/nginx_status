#!/usr/bin/env python
# encoding: utf-8

"""
nginx_stubstatus.py
Prepare Nginx StubStatus page for Monitis
Use MonitisPythonSDK (by Jeremiah Shrik)
Require Python ElementTree Package
Created by Glenn Y. Chen on 2012-01-01.
Copyright (c) 2012 Monitis. All rights reserved.
"""

import urllib2
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-u', metavar='<status url>', default='http://localhost/status', help='the name of the network interface - defaults to "http://localhost/status"')
parser.add_argument('-p', metavar='<check prefix>', default='nginx', help='prefix/name to assign the values to - defaults to "nginx"')

args = parser.parse_args()
#print args

status_url = args.u
prefix = args.p



class NginxStubStatus:
    def __init__(self, status_url):
        #todo: if the page url is not good, throw exception
        self.status_url = status_url
        self.ACTIVE_CONNECT = ""
        self.ACCEPT = ""
        self.HANDLED_CONNECT = ""
        self.HANDLED_REQ = ""
        self.READ = ""
        self.WRITE = ""
        self.WAIT = ""

    def get_nginx_stats_results_for_monitis(self):
        page = self.fetch_nginx_status_page()
        self.parse_nginx_status_page(page)

        gauges = { "active": self.ACTIVE_CONNECT,
                    "accept": self.ACCEPT,
                    "handled":  self.HANDLED_CONNECT,
                    "handles":  self.HANDLED_REQ,
                    "read": self.READ,
                    "write": self.WRITE,
                    "wait": self.WAIT } 
        return gauges

    def fetch_nginx_status_page(self):
        f = urllib2.urlopen(self.status_url)
        return f.read()

    def parse_nginx_status_page(self, page):
        lines = page.split('\n')
        active_connections = lines[0] 
        requests = lines[2]
        read_write_wait = lines[3]

        self.parse_active_connection(active_connections)
        self.parse_request(requests)
        self.parse_read_write_wait(read_write_wait)

    def parse_active_connection(self, line):
        line = line[line.find(':')+2:]
        line = line.strip()
        self.ACTIVE_CONNECT = line

    def parse_request(self, line):
        requests = line.split(' ')
        self.ACCEPT = requests[1]
        self.HANDLED_CONNECT = requests[2]
        self.HANDLED_REQ = requests[3]

    def parse_read_write_wait(self, line):
        line = line.upper()
        line = line.replace('READING', '')
        line = line.replace('WRITING', '')
        line = line.replace('WAITING', '')
        line = line.replace(':', '')
        stats = line.split(' ')
        self.READ = stats[1]
        self.WRITE = stats[3]
        self.WAIT = stats[5]
        
    def getResultParams(self):
        activeConnections = 'ActiveConnect:ActiveConnect:ActiveConnects:2;'
        accept = 'Accept:Accept:Accepts:2;'
        handled = 'Handled:Handled:Handleds:2;'
        handles = 'Handles:Handles:Handle:2;'
        read = 'Read:Read:Reads:2;'
        write = 'Write:Write:Writes:2;'
        wait = 'Wait:Wait:Waits:2;'
        resultParams = wait + write + read + handles + handled + accept + activeConnections;
        return resultParams  


if __name__ == "__main__":
    import sys
    
    nginx = NginxStubStatus(status_url)
 
    result = nginx.get_nginx_stats_results_for_monitis()

    for name, value in result.items():
          print prefix + "." + name, value
