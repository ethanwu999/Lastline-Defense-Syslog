#!/usr/bin/python -u

import socket, re
import sqlite3 as db
from datetime import datetime
from setfw import SetFirewall

def get_block_ip(log):
    if log.find('proto=UDP') != -1 and log.find('dpt=53') != -1 and log.find('dns-resolution') != -1:
        return None
    else:
        match = re.search(r'dst=(.*?) ', log)
        return match.group(1)

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind(('0.0.0.0', 1514))

while True:
#    data, addr = udpSocket.recvfrom()
    data = udpSocket.recv(2048)
#    print '\nReceived message from %s: %s' % (addr, data)
    '''
        1. get time
        2. parse_data for ip address
        3. ip in block list?
            n:
                1. add to block list
                2. config fw
            y:
                update time of ip 
    '''
    #1.
    now = datetime.now()
    #2.
    block_ip = get_block_ip(data)
    if block_ip:
        print 'We got block ip: ' + block_ip
        f = open('block_ip.txt', 'r')
        old_block_ip_file = f.readlines()
        f.close()
        old_block_ip_list = []
        for line in old_block_ip_file:
            (ip, _, _, _, _, _, _) = line.split(' ')
            old_block_ip_list.append(ip)
        new_block_ip_file = []
        # 3.
        newline = ' '.join((block_ip, str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute), str(now.second) + '\n'))
        if block_ip in old_block_ip_list:
            print 'The block ip is in old list'
            #3. update time of ip
            for line in old_block_ip_file:
                (ip, _, _, _, _, _, _) = line.split(' ')
                if block_ip == ip:
                    new_block_ip_file.append(newline)
                else:
                    new_block_ip_file.append(line)
            f = open('block_ip.txt', 'w')
            for item in new_block_ip_file:
                f.write(item)
            f.close()
        else:
            print 'The block ip is NOT in old list'
            #3. add to block list
            f = open('block_ip.txt', 'a')
            f.write(newline)
            f.close()
            #3. config fw
            conn = db.connect('config.db')
            cursor = conn.cursor()
            table = cursor.execute('select * from firewallcfg')
            firewallcfg = table.fetchone()
            conn.close()
            print 'Config Firewall: ' + str(firewallcfg)
            setupfw = SetFirewall(*firewallcfg)
            setupfw.do_config(block_ip)
    else:
        print "We didn't got any block ip"
