#!/usr/bin/env python

import sys
from influxdb import InfluxDBClient

client = InfluxDBClient(host='172.16.231.190',
                        port=8086,
                        username='admin',
                        password='admin123',
                        database='nginx_access_log',
                        timeout=10,
                        retries=5)

try:
    status_code = sys.argv[1]
    query = 'SELECT count(distinct("request_uri")) FROM "four_days"."logstash" WHERE "status" = \'{}\' AND time > now() - 1h;'.format(status_code)
    result = client.query(query)
    result = [a for a in result]
    if result:
        print(result[0][0].get("count", 0))
    else:
        print(0)
except Exception as e:
    pass 

