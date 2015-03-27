#!/usr/bin/python

'''
    This is for clean block ip list every hour

check if time exceed 1hr.
    n: 
        do nothing
    y:
        1. delete ip from block list
        2. remove ip from fw config
'''

from datetime import datetime
from setfw import SetFirewall
import sqlite3 as db

now = datetime.now()
print '-' * 50
print now
f = open('block_ip.txt', 'r')
new_block_ip_file = []
for line in f:
    (ip, year, month, day, hour, minute, second) = line.split(' ')
    ip_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    print (now - ip_time).total_seconds()
    if (now - ip_time).total_seconds() < 3600:
        print 'time not exceed: ' + ip
        new_block_ip_file.append(line)
    else:
        # unconfig fw
        conn = db.connect('config.db')
        cursor = conn.cursor()
        table = cursor.execute('select * from firewallcfg')
        firewallcfg = table.fetchone()
        conn.close()
        print 'Config FW'
        setupfw = SetFirewall(*firewallcfg)
        setupfw.clean_config(ip)
        # delete from block ip list
f.close()
print new_block_ip_file
f = open('block_ip.txt', 'w')
for item in new_block_ip_file:
    f.write(item)
f.close()
