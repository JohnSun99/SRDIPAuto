import csv
from pprint import pprint

def d_read_host_file(host_file_name = 'host_info.csv'):
        host_file = open(host_file_name, 'r')
        csv_input = csv.reader(host_file)
        d_host_ip = {}
        for host in csv_input:
                if host == []:
                        continue
                host_name = host[0].strip(' ')
                host_mgmt_ip = host[1].strip(' ')
                if host_name not in d_host_ip:
                        d_host_ip[host_name] = host_mgmt_ip
                else:
                        if d_host_ip[host_name] != host_mgmt_ip:
                                print 'Warning!!! duplicate host info' + host_name
        #pprint(d_host_ip)
        host_file.close()
        return d_host_ip


def s_port_id_normalize(port_str):
    port_id = 'Eth'
    port_name = port_str.split('/')
    try:
        fex_index = port_name[0][-3:].strip(' ')
        fex_id = int(fex_index) 
        port_id += fex_index
        port_id += '/1/'
        port_id += port_name[2].strip(' ')
    except:
        port_id += '1/'
        port_id += port_name[1].strip(' ')
    return port_id

def l_parse_vlans(var_s_vlans):
        l_all_vlans = []
        l_vlan_comma = var_s_vlans.split(',')
        for entry in l_vlan_comma:
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


###     input format of req csv
#0      Switch Hostname,
#1      port,
#2      vlans,
#3      Port Description,
#4      "access or trunk(access)",
#5      "vpc(none)",
#6      "mtu(9216)",
#7      "speed(auto)",
#8      "duplex(auto)",
#9      "shutdown(no)",
#10     "overwrite(no)"

### ouput format , it is a hostname:l_ports, each_port is port_ID: d_port_detail
#       {'CBPDCNCL-N09IRH2-RT17': [{'Eth1/6': {'desc': 'SLAC-UPD-Splunk 1-Prod#1 10.30.132.2',
#                                            'duplex': 'auto',
#                                            'mode': 'access',
#                                            'mtu': 9216,
#                                            'overwrite': 'no',
#                                            'shutdown': 'no',
#                                            'speed': 'auto',
#                                            'vlans': [132],
#                                            'vpc': 0}},
#                                                               ...
#                                  {'Eth103/1/13': {'desc': 'SLAC-UPD-SplunkV3 Production1',
#                                             'duplex': 'auto',
#                                             'mode': 'access',
#                                             'mtu': 9216,
#                                             'overwrite': 'no',
#                                             'shutdown': 'no',
#                                             'speed': 'auto',
#                                             'vlans': [133],
#                                             'vpc': 0}}],
#        ...
#        'CBPDCNFL-N48GE2A-RT01': [{'Eth1/44': {'desc': 'SLAC-UPD-beaunsw083-DATA-CM0154839',
#                                               'duplex': 'auto',
#                                               'mode': 'trunk',
#                                               'mtu': 9216,
#                                               'overwrite': 'no',
#                                               'shutdown': 'no',
#                                               'speed': 'auto',
#                                               'vlans': [64,
#                                                         65,
#                                                                                                         ...
#                                                         777],
#                                               'vpc': 0}}]
#       }

def d_read_uni_req(req_file_name):
        req_file = open(req_file_name, 'r')
        csv_input = csv.reader(req_file)
        i = 0
        d_uni_req = {}
        for line in csv_input:
                i += 1
                #skip csv header
                if i <= 6:
                        continue
                else:
                        # skip empty line
                        if line == []:
                                continue

                        temp_name = line[0].strip(' ')
                        temp_port_id = line[1].strip(' ')

                        # skip as an empty line if no host and no port_id
                        if (temp_name == '') and (temp_port_id == ''):
                                continue
                        port_id = s_port_id_normalize(temp_port_id)

                        if temp_name != '':
                                host_name = temp_name

                        if host_name not in d_uni_req:
                                d_uni_req[host_name] = []
                        d_each_port = {}
                        d_port_req_details = {}

                        port_mode = line[4].strip(' ')
                        if port_mode == '':
                                d_port_req_details['mode'] = 'access'
                        else:
                                d_port_req_details['mode'] = port_mode

                        port_vlans = line[2].strip(' ')
                        d_port_req_details['vlans'] = l_parse_vlans(port_vlans)
                        if len(d_port_req_details['vlans']) >= 2 :
                                d_port_req_details['mode'] = 'trunk'

                        d_port_req_details['desc'] = line[3].strip(' ')

                        port_vpc = line[5].strip()
                        if port_vpc == '':
                                d_port_req_details['vpc'] = 0
                        else:
                                d_port_req_details['vpc'] = int(port_vpc)

                        port_mtu = line[6].strip(' ')
                        if port_mtu == '':
                                d_port_req_details['mtu'] = 9216
                        else:
                                d_port_req_details['mtu'] = int(port_mtu)

                        port_speed = line[7].strip(' ')
                        if port_speed == '':
                                d_port_req_details['speed'] = 'auto'
                        else:
                                d_port_req_details['speed'] = port_speed

                        port_duplex = line[8].strip(' ')
                        if port_duplex == '':
                                d_port_req_details['duplex'] = 'auto'
                        else:
                                d_port_req_details['duplex'] = port_duplex

                        port_admin_status = line[9].strip(' ')
                        if port_admin_status == '':
                                d_port_req_details['shutdown'] = 'no'
                        else:
                                d_port_req_details['shutdown'] = port_admin_status

                        port_overwrite = line[10].strip(' ')
                        if port_overwrite == '':
                                d_port_req_details['overwrite'] = 'no'
                        else:
                                d_port_req_details['overwrite'] = port_overwrite

                        #pprint(d_port_req_details)
                        d_each_port[port_id] = d_port_req_details
                        d_uni_req[host_name].append(d_each_port)
        req_file.close()
        #pprint(d_uni_req)
        return d_uni_req

def d_get_switch_vPC_list(d_uni_req):
    d_req_vPCs = {}
    for host_name, port_list in d_uni_req.items():
        d_req_vPCs[host_name] = []
        for each_port in port_list:
            for port, port_details in each_port.items():
                temp_vpc = port_details['vpc']
                if (temp_vpc != 0) and (temp_vpc not in d_req_vPCs[host_name]):
                    d_req_vPCs[host_name].append(temp_vpc)
        d_req_vPCs[host_name].sort()
    return d_req_vPCs

def d_get_switch_req_vlan_list(d_uni_req):
        d_req_vlans = {}
        for host_name, port_list in d_uni_req.items():
                d_req_vlans[host_name] = []
                for each_port in port_list:
                        for port, port_details in each_port.items():
                                for each_vlan in port_details['vlans']:
                                        if each_vlan not in d_req_vlans[host_name]:
                                                d_req_vlans[host_name].append(each_vlan)
                d_req_vlans[host_name].sort()
        return d_req_vlans

def d_get_peer_req_vlan_list(d_peers, d_req_vlans):
        d_peer_req_vlans = {}
        for each_switch in d_peers.keys():
                peer_switch = d_peers[each_switch]
                d_peer_req_vlans[each_switch] = d_req_vlans[each_switch]
                if peer_switch in d_req_vlans.keys():
                        for each_vlan in d_req_vlans[peer_switch]:
                                if each_vlan not in d_peer_req_vlans[each_switch]:
                                        d_peer_req_vlans[each_switch].append(each_vlan)

        return d_peer_req_vlans