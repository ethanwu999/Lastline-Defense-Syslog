#!/usr/bin/python

from getpass import getpass
from crontab import CronTab
from setfw import SetFirewall
from sys import exit
import sqlite3 as db



def get_ssh_pass():
    while True:
        ssh_password1 = getpass('SSH password? ')
        ssh_password2 = getpass('Retype password: ')
        if ssh_password1 == ssh_password2:
            break
        else:
            print '\nPassword not match, try again!\n'
    return ssh_password1

title = '''
Lastline Defense Syslog (LDS) Config Menu
'''
print title

fw_brand_menu = '''
        Firewall Brand?
        1. Fortigate
        2. Sonicwall
        3. Watchguard
        4. PaloAlto
        
        0. Quit
        
Enter choice: '''

fw_brand_num = input(fw_brand_menu)
if fw_brand_num == 0:
    exit()
elif fw_brand_num == 1:
    fw_brand = 'FG'
elif fw_brand_num == 2:
    fw_brand = 'SW'
elif fw_brand_num == 3:
    fw_brand = 'WG'
elif fw_brand_num == 4:
    fw_brand = 'PA'

fw_ssh_ip = raw_input('Firewall SSH ip? ')
fw_ssh_port = raw_input('Firewall SSH port? ')
fw_ssh_username = raw_input('SSH username? ')
fw_ssh_password = get_ssh_pass()
#print brand_num, ssh_ip, ssh_port, ssh_username, ssh_password
conn = db.connect('config.db')
cursor = conn.cursor()
cursor.execute("drop table if exists firewallcfg")
cursor.execute("create table firewallcfg(fw_brand text, fw_ssh_ip text, fw_ssh_port text, fw_ssh_username text, fw_ssh_password text)")
rowdata = (fw_brand, fw_ssh_ip, fw_ssh_port, fw_ssh_username, fw_ssh_password)
cursor.execute('insert into firewallcfg values(?, ?, ?, ?, ?)', rowdata)
conn.commit()
conn.close()

# set crontab
my_cron = CronTab(user=True)
cronjob = 'cd /home/lastline/lds && ./clean_blocked.py >> /var/log/lastline/clean_blocked.log 2>&1'
my_cron_job = my_cron.new(cronjob)
my_cron_job.enable()
my_cron.write()

print '\n\nLDS Started !!!\n'
