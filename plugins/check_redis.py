#!/usr/bin/env python
# gracefully taken from https://gist.github.com/zircote/6161466 with some modifications
# does not work yet.

# it's not possible to name this file redis.py because redis-py has the same name, so you have to work with namespaces in the config.

import redis

#: redis info keys
VALUES = [
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






def collect(host="127.0.0.1",port=6379,auth=None):
    redis_conn = redis.StrictRedis(host,port,0,auth)
    info = redis_conn.info()
    gauges = {}
    keys_total = 0
    expires_total = 0
    for n in VALUES:
        if n in info:
            gauges[n] = info[n]
    for key in info:
        if key[0:2] == 'db':
            gauges['expires.%s' % key] = info[key]['expires']
            gauges['keys.%s' % key]= info[key]['keys']
            keys_total = keys_total + int(info[key]['keys'])
            expires_total = expires_total + int(info[key]['expires'])
    gauges['expires.total']= expires_total
    gauges['keys.total']= keys_total

    return gauges

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser('retrieve redis values from INFO')
    parser.add_argument("--host", type=str, metavar='<ip/host>', default='localhost', help="the IP/hostname of your redis server")
    parser.add_argument("--port", type=int, metavar='<port>', default=6379, help="the port of your redis server")
    parser.add_argument("--auth", type=str, metavar='<password>', default=None, help="a password, if specified in 'requirepass' ")
    args = parser.parse_args()
    collect(args.host, args.port, args.auth)
