[root@CBPDCNMG-N48GE2B-SR01-DCNM v11]# cat dcnswitch.py
import paramiko
import json
from pprint import pprint

class DCNSwitch():
    def __init__(self, ip, user='ACOE-DCN_P_DCNM', pw='21588Sp5520A7315'):
        self.mgmt_ip = ip
        self.username = user
        self.password = pw
        self.init_basic()

    def init_basic(self):
        self.connect()
        self.get_hostname()
        self.get_vxlans()
        self.get_vlan_brief_info()
        self.get_cdp_neighbour()
        self.get_peer()
        #self.get_port_conf_status()
        self.connect_close()

    def connect(self):
        self.session = paramiko.SSHClient()
        self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.session.connect(hostname=self.mgmt_ip, username=self.username, password=self.password)

    def get_hostname(self):
        stdin, stdout, stderr = self.session.exec_command('show hostname')
        cli_output = stdout.readlines()
        self.hostname = cli_output[0].split('.')[0]
        self.role = self.hostname[6:8]

    def get_vxlans(self):
        stdin, stdout, stderr = self.session.exec_command('show vxlan')
        cli_output = stdout.readlines()
        vlan_table = {}
        for line in cli_output[2:]:
            key, value = str(line).strip('\n').split('\t\t')
            vlan_id = int(key)
            vxlan_id = int(value)
            if vlan_id not in vlan_table:
                vlan_info = {}
                vlan_info['vxlan_id'] = vxlan_id
                vlan_table[vlan_id] = vlan_info
        self.vlans = vlan_table


    def get_vlan_brief_info(self):
        stdin, stdout, stderr = self.session.exec_command('show vlan brief | json')
        cli_output = stdout.readlines()
        s_cli_out = str(cli_output[0])
        j_cli_out = json.loads(s_cli_out)
        for each_vlan in j_cli_out["TABLE_vlanbriefxbrief"]["ROW_vlanbriefxbrief"]:
            vlan_id = int(each_vlan["vlanshowbr-vlanid"])
            if vlan_id in self.vlans:
                self.vlans[vlan_id]["vlan_name"] = str(each_vlan["vlanshowbr-vlanname"])

    def connect_close(self):
        self.session.close()

    def get_cdp_neighbour(self):
        stdin, stdout, stderr = self.session.exec_command('show cdp nei | json')
        cli_output = stdout.readlines()
        #print '\n' *3
        #print self.hostname
        #print '\n' * 2
        #print cli_output
        self.cdp_neighbours = {}
        if len(cli_output) == 0:
                print "Warning!!!! Please enable cdp neighbour on switch " + self.hostname
                self.session.close()
                exit()
        s_cli_out = str(cli_output[0])
        j_cli_out = json.loads(s_cli_out)
        for each_neighbor in j_cli_out["TABLE_cdp_neighbor_brief_info"]["ROW_cdp_neighbor_brief_info"]:
            neighbor_table = {}
            neighbor_table["hostname"] = str(each_neighbor["device_id"].split('.')[0])
            self.cdp_neighbours[str(each_neighbor["intf_id"])] = neighbor_table

    def get_peer(self):
        if self.role in ['CL', 'FL', 'NL', 'ML', 'NC']:
            if 'Ethernet1/53' in self.cdp_neighbours:
                self.peer = self.cdp_neighbours['Ethernet1/53']['hostname']
            elif 'Ethernet1/54' in self.cdp_neighbours:
                self.peer = self.cdp_neighbours['Ethernet1/54']['hostname']
        elif self.role in ['DL', 'DR']:
            if 'Ethernet1/35' in self.cdp_neighbours:
                self.peer = self.cdp_neighbours['Ethernet1/35']['hostname']
            elif 'Ethernet1/36' in self.cdp_neighbours:
                self.peer = self.cdp_neighbours['Ethernet1/36']['hostname']

    def get_port_conf_status(self):
        self.ports_configured = {}
        if self.role in ['CL', 'FL', 'NL', 'ML', 'NC']:
            for port_index in range(1,45):
                port_id = 'Ethernet1/' + str(port_index)
                stdin, stdout, stderr = self.session.exec_command('show runn inter Ethernet1/' + str(port_index))
                cli_output = stdout.readlines()
                #pprint(cli_output)
                if cli_output[7].strip('\n') != '':
                   self.ports_configured[port_id] = 'yes'
                   if (self.role == 'NC') and (port_index % 2 == 0): 
                        for sub_index in range(1, 49):
                            fex_port_id = 'Ethernet' + str(100 + port_index / 2) + '/1/' + str(sub_index)
                            #print fex_port_id
                            stdin, stdout, stderr = self.session.exec_command('show runn inter ' + fex_port_id)
                            cli_output = stdout.readlines()
                            #print cli_output
                            if cli_output[7].strip('\n') != '':
                                self.ports_configured[fex_port_id] = 'yes'
                            else:
                                self.ports_configured[fex_port_id] = 'no'
                else:
                    self.ports_configured[port_id] = 'no'
        elif self.role in ['DL', 'DR']:
            for port_index in range(1,27):
                port_id = 'Ethernet1/' + str(port_index)
                stdin, stdout, stderr = self.session.exec_command('show runn inter Ethernet1/' + str(port_index))
                cli_output = stdout.readlines()
                if cli_output[7].strip('\n') != '':
                    self.ports_configured[port_id] = 'yes'
                else:
                    self.ports_configured[port_id] = 'no'
        #pprint(self.ports_configured)

    def check_ports_status(self, port_list):
        self.connect()
        #print 'checking ports status .....' + self.hostname
        #pprint(port_list)
        configured_port_details = {}
        for each_port_member in port_list:
            for each_port, details in each_port_member.items():
                #pprint(each_port)
                stdin, stdout, stderr = self.session.exec_command('show runn inter ' + each_port)
                cli_output = stdout.readlines()
                try:
                    if str(cli_output[7]).strip('\n') != '':
                        #print(str(cli_output[7]).strip('\n'))
                        configured_port_details[each_port] = {}
                        configured_port_details[each_port]['configured'] = 'yes'
                        configured_port_details[each_port]['running_config']=[]
                        for line in cli_output[6:]:
                            configured_port_details[each_port]['running_config'].append(str(line).strip('\n'))
                        stdin, stdout, stderr = self.session.exec_command('show inter ' + each_port)
                        cli_output_up = stdout.readlines()
                        port_status_output = str(cli_output_up[0])
                        #print port_status_output
                        if 'up' in port_status_output:
                            configured_port_details[each_port]['up'] = 'yes'
                        else:
                            #print 'not up'
                            configured_port_details[each_port]['up'] = 'no'
                        #pprint(configured_port_details)
                except:
                    continue
        self.connect_close()
        #pprint(l_configured_port)
        return configured_port_details
[root@CBPDCNMG-N48GE2B-SR01-DCNM v11]# 