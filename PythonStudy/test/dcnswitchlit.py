import paramiko
import json
from pprint import pprint
import time

class DCNSwitch():
    def __init__(self, ip, user='ACOE-DCN_P_DCNM', pw='21588Sp5520A7315'):
        self.mgmt_ip = ip
        self.username = user
        self.password = pw
        self.get_inventory()
        self.get_hostname()

    def general_check(self, cli):
        self.connect()
        if 'json' not in cli:
            stdin, stdout, stderr = self.session.exec_command(cli)
            cli_output = stdout.readlines()
            self.connect_close()
            return cli_output
        else:
            i = 1
            while i < 5:
                try:
                    stdin, stdout, stderr = self.session.exec_command(cli)
                    cli_output = stdout.readlines()
                    str1 = ''.join(cli_output)
                    d_cli_output = json.loads(str1)
                    i = 5
                    self.connect_close()
                    return d_cli_output
                except:
                    print str(i) + 'th collecting info from ' + self.mgmt_ip + ' failed, and trying again'
                    i += 1
                    time.sleep(i * 1)
            s_error_message = "Login-Failed"
            return (False)
        
    def connect(self):
        #print '\n' * 2
        #print 'Connecting to ' + self.mgmt_ip
        try:
            self.session = paramiko.SSHClient()
            self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.session.connect(hostname=self.mgmt_ip, username=self.username, password=self.password)
        except:
            print 'can not login to ' + self.mgmt_ip
            
    def connect_close(self):
        self.session.close()
        
    def get_hostname(self):
        cli = 'show hostname | json-pretty'
        jd = self.general_check(cli)
        self.hostname = jd["hostname"].split('.')[0]
        #self.role = self.hostname[6:8]
        
    def get_inventory(self):
        cli = 'show inventory | json-pretty'
        jd = self.general_check(cli)
        self.HWPlatform = jd["TABLE_inv"]["ROW_inv"][0]["productid"]

