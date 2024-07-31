import paramiko
import json
from pprint import pprint
import time

class iosSwitch():
    def __init__(self, ip, user='d368451', pw='Za9QianD'):
        self.mgmt_ip = ip
        self.username = user
        self.password = pw

    def general_check(self, cli):
        self.connect()
        stdin, stdout, stderr = self.session.exec_command(cli)
        cli_output = stdout.readlines()
        self.connect_close()
        return cli_output

    def connect(self):
        #print '\n' * 2
        print 'Connecting to ' + self.mgmt_ip
        self.session = paramiko.SSHClient()
        self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        i = 1
        while i < 4:
            try:
                self.session.connect(hostname=self.mgmt_ip, username=self.username, password=self.password)
                i = 4
            except:
                print str(i) + 'th login to ' + self.mgmt_ip + ' failed, and trying again'
                i += 1
                time.sleep(2)

    def connect_close(self):
        self.session.close()
