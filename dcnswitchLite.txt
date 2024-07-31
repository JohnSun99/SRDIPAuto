[root@CBPDCNMG-N48GE2B-SR01-DCNM v11]# cat dcnswitchLite.py
import paramiko
import json
from pprint import pprint

class DCNSwitch():
    def __init__(self, ip, user='ACOE-DCN_P_DCNM', pw='21588Sp5520A7315'):
        self.mgmt_ip = ip
        self.username = user
        self.password = pw

    def general_check(self, cli):
        self.connect()
        self.get_hostname()
        stdin, stdout, stderr = self.session.exec_command(cli)
        cli_output = stdout.readlines()
        self.connect_close()
        return cli_output

    def connect(self):
        #print '\n' * 2
        #print 'Connecting to ' + self.mgmt_ip
        try:
            self.session = paramiko.SSHClient()
            self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.session.connect(hostname=self.mgmt_ip, username=self.username, password=self.password)
        except:
            print 'can not login to ' + self.mgmt_ip

    def get_hostname(self):
        stdin, stdout, stderr = self.session.exec_command('show hostname')
        cli_output = stdout.readlines()
        self.hostname = cli_output[0].split('.')[0]
        self.role = self.hostname[6:8]

    def connect_close(self):
        self.session.close()

[root@CBPDCNMG-N48GE2B-SR01-DCNM v11]# 