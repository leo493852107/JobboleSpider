#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

redis_cli = redis.StrictRedis("localhost")

redis_cli.incr("jobbole_count")
