#!/usr/bin/env python
import redis
red = redis.Redis()
print red.info()
