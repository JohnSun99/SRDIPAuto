from dcnswitchLite import *
from iosswitchLite import *
import gen_funs
from pprint import pprint
from collections import namedtuple
import csv
import datetime

d_host_ip = gen_funs.d_read_host_file()
while True:
    # Read in existing vlan, mac and IP info
    d_mac_ip = {}
    ll_item = []
    Keys = namedtuple('vlan_mac', 'Vlan_ID Mac_Add')
    with open("arp_DC_all.csv", "rb") as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip the headers
        for row in reader:
            vlanID = int(row[0])
            Mac = row[1]
            key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
            if key1 not in d_mac_ip:
                d_mac_ip[key1] = {}
                d_mac_ip[key1]["IP"] = row[2]
                d_mac_ip[key1]["Type"] = row[3]
                d_mac_ip[key1]["Location"] = row[4]
    
    l_hosts = open('task_GWList_NOVRF.txt', 'r')
    for line in l_hosts:
        l_host_info = line.strip('\n').split(',')
        gw_name = l_host_info[0]
        gw_type = l_host_info[1]
        gw_location = l_host_info[2]
        gw_vrf = 'YES' in l_host_info[3]
        switch1 = iosSwitch(d_host_ip[gw_name])
        
        #cli = "show mac address-table | i Yes"
        #output = switch1.general_check(cli)
        #
        #for each_item in output:
        #    each_mac = str(each_item)
        #    vlanID = int(each_mac[3:6].strip(' '))
        #    Mac = each_mac[8:22]
        #    #Intf = each_mac[51:].strip('\n').strip('\r')
        #    key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
        #    #pprint(key1)
        #    if key1 not in d_mac_ip:
        #        d_mac_ip[key1] = {}
        #        d_mac_ip[key1]["Type"] = gw_type
        #        d_mac_ip[key1]["Location"] = gw_location      
        
        if gw_vrf :
            cli = "show ip vrf | i CommSec|SAP|RBB"
            output = switch1.general_check(cli)
            l_ip_vrf = gen_funs.l_get_IOS_vrf(output)
            for each_vrf in l_ip_vrf:
                cli = "show ip arp vrf " + each_vrf + " | i Vlan"
                #print cli
                output = switch1.general_check(cli)
                
                for each_item in output:
                    each_arp = str(each_item).strip('\n').strip('\r')
                    s_vlanID = each_arp[65:]
                    vlanID = int(s_vlanID)
                    if vlanID == 0:
                        continue
                    Mac = each_arp[38:52]
                    IP = each_arp[10:30].strip(' ')
                    key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
                    #pprint(key1)
                    if key1 not in d_mac_ip:
                        d_mac_ip[key1] = {}
                        d_mac_ip[key1]["Type"] = gw_type
                        d_mac_ip[key1]["Location"] = gw_location           
                        d_mac_ip[key1]["IP"] = IP
        else:        
            cli = "show ip arp | i Vlan"
            #print cli
            output = switch1.general_check(cli)
            
            for each_item in output:
                each_arp = str(each_item).strip('\n').strip('\r')
                s_vlanID = each_arp[65:]
                vlanID = int(s_vlanID)
                if vlanID == 0:
                    continue
                Mac = each_arp[38:52]
                IP = each_arp[10:30].strip(' ')
                key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
                #pprint(key1)
                if key1 not in d_mac_ip:
                    d_mac_ip[key1] = {}
                    d_mac_ip[key1]["Type"] = gw_type
                    d_mac_ip[key1]["Location"] = gw_location           
                    d_mac_ip[key1]["IP"] = IP
        #pprint(d_mac_ip)
    
        currentTime = str(datetime.datetime.now())[0:16]
        for key in sorted(d_mac_ip):
            #pprint (key)
            l_item = []
            l_item.append(key.Vlan_ID)
            l_item.append(key.Mac_Add)
            l_item.append(d_mac_ip[key]['IP'])
            l_item.append(d_mac_ip[key]['Type'])
            l_item.append(d_mac_ip[key]['Location'])
            l_item.append(currentTime)
            ll_item.append(l_item)
        
    l_hosts.close()
    with open("arp_DC_all.csv",'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Vlan_ID', 'MAC', 'IP', 'Type', 'Location','Time'])
        writer.writerows(ll_item)
        
    time.sleep(20)
