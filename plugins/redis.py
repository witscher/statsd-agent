#!/usr/bin/env python
# gracefully taken from https://gist.github.com/zircote/6161466
import statsd
import time
import argparse
import sys
import os
import redis

#: redis info keys
GAUGES = [
    'used_memory',
    'used_memory_lua',
    'used_memory_rss',
    'mem_fragmentation_ratio',
    'pubsub_channels',
    'pubsub_patterns',
    'rdb_saves',
    'rdb_changes_since_last_save',
    'aof_last_rewrite_time_sec',
    'aof_last_rewrite_time_sec',
    'blocked_clients',
    'aof_rewrites',
    'client_biggest_input_buf',
    'client_longest_output_list',
    'connected_clients',
    'connected_slaves',
    'evicted_keys',
    'expired_keys',
    'latest_fork_usec',
    'instantaneous_ops_per_sec',
    'rdb_last_bgsave_time_sec',
    'rdb_changes_since_last_save',
    'rdb_current_bgsave_time_sec',
    'total_commands_processed',
    'total_connections_received',
    'rejected_connections',
    'used_memory_peak',
    'used_cpu_sys',
    'used_cpu_sys_children',
    'used_cpu_user',
    'used_cpu_user_children',
    'keyspace_read_hits',
    'keyspace_read_misses',
    'keyspace_write_hits',
    'keyspace_write_misses',
]


parser = argparse.ArgumentParser('A python script to monitor and submit statistics to a statsd endpoint')
parser.add_argument("-s", "--server", type=str, default='localhost:6379',
                    help="the server(s) ',' delimited to collect stats from example:[test.com:6379,test.com]")
parser.add_argument("--namespace-service", help="the service namespace key for statsd",
                    default='redis', type=str)
parser.add_argument("-v", "--verbose", help="print the statsd namespaces being monitored", action="store_true")
parser.add_argument("-f", "--frequency", help="frequency to collect statistics in seconds [1]", default=1, type=int)
parser.add_argument("--statsd-host", help="statsd server address", default="127.0.0.1", type=str)
parser.add_argument("--statsd-port", help="statsd server port", default=8125, type=int)
parser.add_argument("--statsd-sample-rate", help="statsd sample rate", default=1, type=int)
parser.add_argument("--detach", help="detach process and run in background", action="store_true")
parser.add_argument("-l", "--loglevel", help="enable debugging", choices=('DEBUG', 'INFO', 'ERROR', 'CRITICAL', 'FATAL'),
                    default="INFO")
parser.add_argument("--namespace-format", default="{host}.{service_name}.{port}", type=str,
                    help="the namespace key format")
args = parser.parse_args()

redis_conn = redis.StrictRedis()
info = redis_conn.info()
print info

def collect():
    redis_conn = redis.StrictRedis()
    info = redis_conn.info()
    log_gauges(redis_conn, info)




def log_gauges(ns, info):
    keys_total = 0
    expires_total = 0
    for n in GAUGES:
        if n in info:
            print('redis.'+ n, info[n])
    for key in info:
        if key[0:2] == 'db':
            print('redis.expires.%s' % key, info[key]['expires'])
            print('redis.keys.%s' % key, info[key]['keys'])
            keys_total = keys_total + int(info[key]['keys'])
            expires_total = expires_total + int(info[key]['expires'])
    print('redis.expires.total', expires_total)
    print('redis.keys.total', keys_total)

if __name__ == "__main__":
    import sys
    collect()
    

