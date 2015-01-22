Lastline-Defense-Syslog
=======================
The whole concept is to block the first seen C&C connection with specific score.

This is a syslog server, listening on UDP port 1514. Even though it's a syslog server,
but only work for Lastline log, and just for C&C(callback) log. There are two kinds of
C&C log from Lastline: DNS query and C&C connection. This system will ignore DNS query,
and will only process C&C connection log to extract the destination IP address which
will become one of the block-list item of the firewall or IPS.

Lastline Config:
Admin -> Reporting -> Notifications

LDS Config:
1. ip
sudo vi /etc/network/interfaces
sudo /etc/init.d/networking restart
2. timezone
sudo dpkg-reconfigure tzdata
cat /etc/timezone
3. ntp
sudo ntpdate <ntp server>
4. config.py
cd /etc/lds
./config.py


