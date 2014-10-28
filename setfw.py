#!/usr/bin/python

import paramiko, time, sys

class SetFirewall:
    def __init__(self, brand, ssh_ip, ssh_port, ssh_username, ssh_password):
        self.brand = brand
        self.ssh_ip = ssh_ip
        self.ssh_port = int(ssh_port)
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        
    def _fg_ip_to_config(self, badip, _mode):
        _addr_cmds = ['', 'config firewall address', 'end', '']
        _adgp_cmds = ['', 'config firewall addrgrp', 'edit "LastLine_Deny"', 'end', '']
        _ip = badip
        _llip = 'll_' + _ip
        if _mode == 'edit':
            _set_host = 'edit ' + _llip
            _set_subnet = 'set subnet ' + _ip + '/32'
            _addr_cmds.insert(2, _set_subnet)
            _addr_cmds.insert(2, _set_host)
            _set_member = 'set member ' + _llip
            _adgp_cmds.insert(3, _set_member)
            _cmds = _addr_cmds + _adgp_cmds
        elif _mode == 'delete':
            _delete_host = 'delete ' + _llip
            _set_member = 'set member _tmp'
            _addr_cmds.insert(2, _delete_host)
            _adgp_cmds.insert(3, _set_member)
            _cmds = _adgp_cmds + _addr_cmds
        _cmds.insert(-1, 'exit')
        _scmds = '\n'.join(_cmds)
        return _scmds
    
    def _sw_ip_to_config(self, badip, _mode):
        _cmds = [self.ssh_username, self.ssh_password, 'configure', 'y']
        _ip = badip
        _llip = 'll_' + _ip
        if _mode == 'edit':
            _addobj = 'address-object ' + _llip
            _host = 'host ' + _ip
            _zone = 'zone WAN'
            _end = 'end'
            _addgrp = 'address-group LastLine_Deny'
            _cmds.append(_addobj)
            _cmds.append(_host)
            _cmds.append(_zone)
            _cmds.append(_end)
            _cmds.append(_addgrp)
            _cmds.append(_addobj)
            _cmds.append(_end)
        elif _mode == 'delete':
            _noobj = 'no ' + 'address-object ' + _llip
            _cmds.append(_noobj)
        _cmds.append('end\nexit\n')
        _scmds = '\n'.join(_cmds)
        return _scmds
        
    def _wg_ip_to_config(self, badip, _mode):
        _cmds = ['', 'configure', 'exit', '']
        if _mode == 'edit':            
            _block_host = 'ip blocked-site host '
        elif _mode == 'delete':            
            _block_host = 'no ip blocked-site host '
        _ip = badip
        _block_host = _block_host + _ip
        _cmds.insert(2, _block_host)
        _scmds = '\n'.join(_cmds)
        return _scmds

    def _pa_ip_to_config(self, badip, _mode):
        _cmds = ['', 'configure', 'save config', 'commit', 'exit', 'exit', '']
        _ip = badip
        _llip = 'll_' + _ip
        if _mode == 'edit':            
            _set_host = 'set address ' + _llip + ' ip-netmask ' + _ip + '/32'
            _set_group = 'set address-group LastLine_Deny ' + _llip
            _cmds.insert(2, _set_group)
            _cmds.insert(2, _set_host)
        elif _mode == 'delete':            
            _delete_group = 'delete address-group LastLine_Deny ' + _llip
            _delete_host = 'delete address ' + _llip
            _cmds.insert(2, _delete_host)
            _cmds.insert(2, _delete_group)
        _scmds = '\n'.join(_cmds)
        return _scmds

    def do_config(self, badip):
        _mode = 'edit'
        _ssh = paramiko.SSHClient()
        _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.brand == 'FG':
            _scmds = self._fg_ip_to_config(badip, _mode)
        elif self.brand == 'WG':
            _scmds = self._wg_ip_to_config(badip, _mode)
        elif self.brand == 'PA':
            _scmds = self._pa_ip_to_config(badip, _mode)
        elif self.brand == 'SW':
            _scmds = self._sw_ip_to_config(badip, _mode)
            self.ssh_username = ''
            self.ssh_password = ''
        print _scmds
        _sleep_time = 3
        try:
            _ssh.connect(self.ssh_ip, port=self.ssh_port, username=self.ssh_username, password=self.ssh_password)
            _chan = _ssh.invoke_shell()
            _chan.sendall(_scmds)
            time.sleep(_sleep_time)
            print _chan.recv(1024000)
            _chan.close()
        except:
            print 'WARNING: Unable ssh to firewall !!!'
        _ssh.close()        

    def clean_config(self, badip):
        _mode = 'delete'
        _ssh = paramiko.SSHClient()
        _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.brand == 'FG':
            _scmds = self._fg_ip_to_config(badip, _mode)
        elif self.brand == 'WG':
            _scmds = self._wg_ip_to_config(badip, _mode)
        elif self.brand == 'PA':
            _scmds = self._pa_ip_to_config(badip, _mode)
        elif self.brand == 'SW':
            _scmds = self._sw_ip_to_config(badip, _mode)
            self.ssh_username = ''
            self.ssh_password = ''
        print _scmds
        _sleep_time = 3
        try:
            _ssh.connect(self.ssh_ip, port=self.ssh_port, username=self.ssh_username, password=self.ssh_password)
            _chan = _ssh.invoke_shell()
            _chan.sendall(_scmds)
            time.sleep(_sleep_time)
            print _chan.recv(1024000)
            _chan.close()
        except:
            print 'WARNING: Unable ssh to firewall !!!'
        _ssh.close()        

        
def main():
    setupfw = SetFirewall('PA', '1.1.1.1', '2222', 'sshusername', 'sshpassword')
    scmds = setupfw._pa_ip_to_config('5.5.5.5', 'delete')
    print scmds
    
if __name__ == '__main__':
    main()
