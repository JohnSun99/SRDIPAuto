from dcnswitchLite import *
import gen_funs
from pprint import pprint
from collections import namedtuple
import csv

def f_N9K_OSPF_check (l_nbr, site_location):
    d_cdp = {}
    s_peer1_cdp = 'peer1'
    s_peer2_cdp = 'peer2'
    l_up_peer_port = []
    if site_location == 'NW':
        s_sp1 = "10.250.252.1"
        s_sp2 = "10.250.252.2"
        s_sp3 = "10.250.252.3"
        s_sp4 = "10.250.252.4"
    else:
        s_sp1 = "10.246.252.1"
        s_sp2 = "10.246.252.2"
        s_sp3 = "10.246.252.3"
        s_sp4 = "10.246.252.4"
	
 
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
      
def f_print_OSPF_details(swith_ID):
    cli = "show ip OSPF UNDERLAY neighbors"
    output = switch1.general_check(cli)
    pprint(output)
    
def check_DCN_fabric_OSPF(switch_ID):
    print "\nchecking OSPF UNDERLAY Status on " + switch_ID.hostname
    cli = "show ip OSPF UNDERLAY neighbors | i FULL | wc -l"
    jd = switch_ID.general_check(cli)
    if jd == False:
        print "Collecting info from " + switch_ID.hostname + " failed, please try later"
        return False
    pprint(jd)
    if jd[0].strip('\n') != "5":
        f_print_OSPF_details(Switch_ID)
    #l_nbrs = jd["TABLE_ctx"]["ROW_ctx"]["TABLE_nbr"]["ROW_nbr"]
    #if '09IR' in switch_ID.hostname:
    #    s_site_location = 'NW'
    #else:
    #    s_site_location = 'BW'
    #    
    #b_result = f_N9K_OSPF_check (l_nbrs, s_site_location)
    #if not b_result:
    #    f_print_OSPF_details(switch_ID)



if __name__ == "__main__":
    d_host_ip = gen_funs.d_read_host_file()
    l_hosts = open('task_DCN_Health_Check.txt', 'r')
    
    for line in l_hosts:
        switch1 = DCNSwitch(d_host_ip[line.strip('\n')])
        check_DCN_fabric_OSPF(switch1)
    l_hosts.close()
