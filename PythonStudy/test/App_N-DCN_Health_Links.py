from dcnswitchLite import *
import gen_funs
from pprint import pprint
from collections import namedtuple
import csv

d_host_ip = gen_funs.d_read_host_file()
l_hosts = open('task_N-DCN_Health_Links.txt', 'r')

def f_N9K_cdp_check (l_cdp, s_hw_platform, site_location):
    d_cdp = {}
    s_peer1_cdp = 'peer1'
    s_peer2_cdp = 'peer2'
    l_up_peer_port = []
    if site_location == 'NW':
        s_sp1 = "CBPDCNSP-N09IRH1-RT01"
        s_sp2 = "CBPDCNSP-N09IRH1-RT02"
        s_sp3 = "CBPDCNSP-N09IRH2-RT01"
        s_sp4 = "CBPDCNSP-N09IRH2-RT02"
    else:
        s_sp1 = "CBPDCNSP-N48GE2B-RT01"
        s_sp2 = "CBPDCNSP-N48GE2B-RT02"
        s_sp3 = "CBPDCNSP-N48GE2C-RT01"
        s_sp4 = "CBPDCNSP-N48GE2C-RT02"
	
    if s_hw_platform == 'N9K-C9236C':
        port_from = 30
        port_to = 35
        i_peer1 = 35
        i_peer2 = 36
        d_uplink_cdp = {"Ethernet1/31": s_sp1, 
                        "Ethernet1/32": s_sp2, 
                        "Ethernet1/33": s_sp3, 
                        "Ethernet1/34": s_sp4} 
    elif s_hw_platform == 'N9K-C93180LC-EX':
        port_from = 28
        port_to = 33
        i_peer1 = 25
        i_peer2 = 27
        d_uplink_cdp = {"Ethernet1/29": s_sp1, 
                        "Ethernet1/30": s_sp2, 
                        "Ethernet1/31": s_sp3, 
                        "Ethernet1/32": s_sp4}
    else:
        port_from = 48
        port_to = 53
        i_peer1 = 53
        i_peer2 = 54
        d_uplink_cdp = {"Ethernet1/49": s_sp1, 
                        "Ethernet1/50": s_sp2, 
                        "Ethernet1/51": s_sp3, 
                        "Ethernet1/52": s_sp4}         
    for each_cdp in l_cdp:
        if each_cdp["intf_id"] == 'mgmt0':
            continue
        s_port_ID = each_cdp["intf_id"].split('/')[1]

        i_port_ID = int(s_port_ID)
        if (i_port_ID > port_from) and (i_port_ID < port_to):
            d_cdp[each_cdp["intf_id"]] = each_cdp["device_id"].split('.')[0]
            if each_cdp["port_id"] not in l_up_peer_port:
                l_up_peer_port.append(each_cdp["port_id"])  			
        elif i_port_ID == i_peer1:
            s_peer1_cdp = each_cdp["device_id"].split('.')[0]
        elif i_port_ID == i_peer2:
            s_peer2_cdp = each_cdp["device_id"].split('.')[0]
   
    if (cmp(d_cdp, d_uplink_cdp) == 0) and (len(l_up_peer_port) == 1) and (s_peer1_cdp == s_peer2_cdp):
        return True
    else:
        return False                               
      
def f_print_cdp_details(swith_ID):
    cli = "show cdp nei"
    output = switch1.general_check(cli)
    pprint(output)
    
for line in l_hosts:
    switch1 = DCNSwitch(d_host_ip[line.strip('\n')])

    print "\nchecking inter-switch links on " + line.strip('\n')
    cli = "show cdp nei | json"
    jd = switch1.general_check(cli)
    if jd == False:
        print "Collecting info from " + line.strip('\n') + " failed, please try later"
        continue
    l_cdps = jd["TABLE_cdp_neighbor_brief_info"]["ROW_cdp_neighbor_brief_info"]
    if '09IR' in line:
        s_site_location = 'NW'
    else:
        s_site_location = 'BW'
        
    b_result = f_N9K_cdp_check (l_cdps, switch1.HWPlatform, s_site_location)
    if not b_result:
        f_print_cdp_details(switch1)
        
l_hosts.close()
