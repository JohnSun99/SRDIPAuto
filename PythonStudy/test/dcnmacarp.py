from dcnswitchLite import *
import gen_funs
from pprint import pprint
from collections import namedtuple
import csv

d_mac_ip = {}
Keys = namedtuple('vlan_mac', 'Vlan_ID Mac_Add')
with open("arp_DC_all.csv", "rb") as infile:
    reader = csv.reader(infile)
    next(reader, None)  # skip the headers
    for row in reader:
        if row[3] == 'IPNet':
            vlanID = int(row[0]) + 1000
        else:
            vlanID = int(row[0])
        Mac = row[1]
        key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
        if key1 not in d_mac_ip:
            d_mac_ip[key1] = {}
            d_mac_ip[key1]["IP"] = row[2]
            d_mac_ip[key1]["Type"] = row[3]
            d_mac_ip[key1]["Location"] = row[4]

d_host_ip = gen_funs.d_read_host_file()
l_hosts = open('task_dcnleaf_MAC_ARP.txt', 'r')

for line in l_hosts:
    switch1 = DCNSwitch(d_host_ip[line.strip('\n')])
    if 'DCNNC' in line:
        NCLeaf = True
    else:
        NCLeaf = False

    cli = "show ip arp vrf CBA-DCN | json-pretty"
    jd = switch1.general_check(cli)
    try:
        for each_item in jd["TABLE_vrf"]["ROW_vrf"]["TABLE_adj"]["ROW_adj"]:
            vlanID = int(each_item["intf-out"][4:])
            Mac = each_item["mac"]
            key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
            if key1 not in d_mac_ip:
                d_mac_ip[key1] = {}
                d_mac_ip[key1]["IP"] = each_item["ip-addr-out"]
                d_mac_ip[key1]["Type"] = 'DCN'
                if '09IR' in line:
                    d_mac_ip[key1]["Location"] = 'Norwest'
				else:
                    d_mac_ip[key1]["Location"] = 'Burwood'
    except:
        print ''
    
    cli = "show inter status up | json"
    jd = switch1.general_check(cli)
    d_up_port = {}
    for each_port in jd["TABLE_interface"]["ROW_interface"][1:]:
        if (each_port["vlan"] != 'routed') and ('53' not in each_port["interface"]) and ('54' not in each_port["interface"]):
            d_up_port[each_port["interface"]] = each_port["vlan"]
        
    cli = "show inter descrip | json"
    jd = switch1.general_check(cli)
    d_port_info = {}
    for each_port in jd["TABLE_interface"]["ROW_interface"][1:]:
        try:
            s_port = each_port["interface"]
            if NCLeaf:
                if (s_port in d_up_port.keys()) and (('Ethernet10' in s_port) or ('Ethernet11' in s_port)):
                    d_port_info[s_port] = {}
                    d_port_info[s_port]["desc"] = each_port["desc"]
                    d_port_info[s_port]["vlan"] = int(d_up_port[s_port])
            else:
                if (s_port in d_up_port.keys()) and (('Ethernet1' in s_port) or ('port-channel' in s_port)):
                    d_port_info[s_port] = {}
                    d_port_info[s_port]["desc"] = each_port["desc"]
                    d_port_info[s_port]["vlan"] = int(d_up_port[s_port])
			#print '%-20s : %s' % (each_port["interface"], each_port["desc"])
        except:
            continue
        
    #pprint(d_port_info)

    ll_item = []
    cli = "show mac address-table local | json-pretty"
    jd = switch1.general_check(cli)
    for each_port in jd["TABLE_mac_address"]["ROW_mac_address"]:
        s_port = each_port["disp_port"]
        try:
            if s_port in d_port_info.keys() :
                d_port_info[s_port]["mac"] = each_port["disp_mac_addr"]
                l_item = []
                l_item.append(s_port)
                d_port_info[s_port]["vlan"] = int(each_port["disp_vlan"])
                l_item.append(d_port_info[s_port]["vlan"])
                l_item.append(d_port_info[s_port]["mac"])
                try:
                    key1 = Keys(Vlan_ID=d_port_info[s_port]["vlan"], Mac_Add=d_port_info[s_port]["mac"])
                    d_port_info[s_port]["IP"] = d_mac_ip[key1]["IP"]
                    l_item.append(d_port_info[s_port]["IP"])
                    l_item.append(d_mac_ip[key1]["Type"])
                    l_item.append(d_mac_ip[key1]["Location"])
                except:
                    l_item.append('No_IP')
                    l_item.append('Unknown')
                    l_item.append('Unknown')
                l_item.append(d_port_info[s_port]["desc"])
                ll_item.append(l_item)
        except:
            continue
        
    s_filename = line.strip('\n') + '-mac-arp.csv'	
    with open(s_filename,'wb+') as f:
        writer = csv.writer(f)
        writer.writerow(['Port','Vlan_ID', 'MAC', 'IP', 'Type', 'Location', 'Desc'])
        writer.writerows(ll_item)
