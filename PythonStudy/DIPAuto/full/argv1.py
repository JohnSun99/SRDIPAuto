import csv
from sys import argv
from pprint import pprint

def fun_l_parse_vlans(var_s_vlans):
        l_all_vlans = []
        l_vlan_comma = var_s_vlans.split(',')
        for entry in l_vlan_comma:
                #print(entry)
                if '-' in entry:
                        l_group_vlan = entry.split('-')
                        i_begin_vlan = int(l_group_vlan[0])
                        i_end_vlan = int(l_group_vlan[1])
                        while i_begin_vlan <= i_end_vlan:
                                if l_all_vlans.count(i_begin_vlan)==0:
                                        l_all_vlans.extend([i_begin_vlan])
                                i_begin_vlan = i_begin_vlan + 1
                else:
                        i_begin_vlan = int(entry)
                        if l_all_vlans.count(i_begin_vlan)==0:
                                l_all_vlans.extend([i_begin_vlan])
                
        l_all_vlans = sorted(l_all_vlans, key=int)
        return l_all_vlans



if len(argv) == 1:
    print 'format is: python dip source_file'
    exit()

host_file = open('host_info.csv', 'r')
csv_input = csv.reader(host_file)
host_ip_dict = {}
for host in csv_input:
    if host[0] not in host_ip_dict:
        host_ip_dict[host[0]] = host[1]
    else:
        print 'warning!!! duplicate host info' + host[0]
#pprint(host_ip_dict)
host_file.close()

file = open(argv[1], 'r')
csv_input = csv.reader(file)
i = 0
req = {}
for line in csv_input:
    i += 1
    #escapte csv header
    if i == 1:
        continue
    else:
        host_name = line[0]
        #print host_name
        #pprint(host_ip_dict)
        host_ip = host_ip_dict[str(host_name)]
        #print host_ip
        if host_ip not in req:
            req[host_ip] = []
        port_detail = {}              
        port_req = {}

        port_id = line[1].strip(' ')
        
        port_mode = line[4].strip(' ')
        if port_mode == '':
            port_req['mode'] = 'access'
        else:
            port_req['mode'] = line[4].strip(' ')
            
        port_vlans = line[2].strip(' ')
        port_req['vlans'] = fun_l_parse_vlans(port_vlans)
        if len(port_req['vlans']) >= 2 :
            port_req['mode'] = 'trunk'
            
        port_req['desc'] = line[3].strip(' ')
        port_req['vpc'] = line[5].strip()
        
        port_mtu = line[6].strip(' ')
        if port_mtu == '':
            port_req['mtu'] = '9216'
            
        port_speed = line[7].strip(' ')
        if port_speed == '':
            port_req['speed'] = 'auto'
        else:
            port_req['speed'] = port_speed
            
        port_duplex = line[8].strip(' ')
        if port_duplex == '':
            port_req['duplex'] = 'auto'
        else:
            port_req['duplex'] = port_duplex

        port_admin_status = line[9].strip(' ')
        if port_admin_status == '':
            port_req['shutdown'] = 'no shutdown'
        else:
            port_req['shutdown'] = 'shutdown'

        port_overwrite = line[10].strip(' ')
        if port_overwrite == '':
            port_req['overwrite'] = 'no'
        else:
            port_req['shutdown'] = 'yes'
            
        #pprint(port_req)
        port_detail[port_id] = port_req
        req[host_ip].append(port_detail)
file.close()
pprint(req)
